#!/usr/bin/env python
import os, sys, subprocess, re
import argparse
import commands
import time
#____________________________________________________________________________________________________________
### processing the external os commands
def processCmd(cmd, quite = 0):
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    return output


#_____________________________________________________________________________________________________________
#example line: python submitCondorJobs.py --nev 30000 --njobs 500 --maxtime 12h --PU 0
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument ('--nev', help='number of events per job', default=100)
    parser.add_argument ('--njobs', help='number of jobs', default=10)
    parser.add_argument ('--st_seed', help='starting seed', default=1, type=int)

    parser.add_argument ('--PU', help='PU collisions to be generated', default=0, type=int)

#_____________________________________________________________________________________________________________
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central')
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central')

    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTHat3p0-evtgen_HQET2_central')
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTHat5p0-evtgen_HQET2_central')

    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bp_MuNuD10-2420_DmstPi_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central')

    parser.add_argument ('-P', '--process', help='Process name', default='BPH_NoCuts_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central')
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_NoCuts_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central')
#_____________________________________________________________________________________________________________


    parser.add_argument ('--version', help='Process version', default='v0')
    parser.add_argument ('--CMSSW_loc', help='CMSSW src loc', default='/afs/cern.ch/user/o/ocerri/work/generation_CMSSW/CMSSW_10_2_3/src')
    parser.add_argument ('--outdir', help='output directory ', default='/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private')
    parser.add_argument ('--force_production', action='store_true', default=False, help='Proceed even if the directory is already existing')
    parser.add_argument ('--maxtime', help='Max wall run time [s=seconds, m=minutes, h=hours, d=days]', default='8h')
    # parser.add_argument ('--memory', help='min virtual memory', default='8000')
    # parser.add_argument ('--disk', help='min disk space', default='8000')

    args = parser.parse_args()

    nev        = args.nev
    njobs      = int(args.njobs)
    st_seed    = int(args.st_seed)
    cmssw_version = re.search('/CMSSW_[0-9]+_[0-9]+_[0-9]+/src', args.CMSSW_loc).group(0)[7:-4]
    version    = cmssw_version.replace('_', '-') + '_' + args.version
    if args.PU == 0:
        version = 'NoPU_' + version
    elif args.PU > 0:
        version = 'PU{}_'.format(args.PU) + version

    outdir     = args.outdir + '/' + args.process + '_' + version + '/jobs_out'

    time_scale = {'s':1, 'm':60, 'h':60*60, 'd':60*60*24}
    maxRunTime = int(args.maxtime[:-1]) * time_scale[args.maxtime[-1]]
    # mem       = args.memory
    # disk      = args.disk

    mc_frag_dir = args.CMSSW_loc+'/Configuration/GenProduction/python'
    if not os.path.exists(mc_frag_dir):
        os.makedirs(mc_frag_dir)

    mc_frag_name = args.process+'_cfi.py'
    print 'Running process:', args.process
    if not os.path.exists(mc_frag_dir+'/'+mc_frag_name):
        cmd = 'cp '
        cmd += '/eos/user/o/ocerri/BPhysics/MCGeneration/BPH_CMSMCGen/Configuration/GenProduction/python/'
        cmd += mc_frag_name
        cmd += ' '+mc_frag_dir+'/'
        os.system(cmd)
        print 'Compile '+args.CMSSW_loc
        sys.exit()
    else:
        print '--->> I hope you already compiled '+args.CMSSW_loc
        aux = raw_input('Have you? (y/n)\n')
        if 'n' in aux:
            exit()

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        os.makedirs(outdir+'/out/')
        os.makedirs(outdir+'/cfg/')
    elif not args.force_production:
        print 'Output dir: "'+outdir+'" exists.'
        aux = raw_input('Continue anyway? (y/n)\n')
        if aux == 'n':
            exit()

    os.system('chmod +x job1023_gen_NoPU_v1.sh')
    print 'Creating submission script'

    fsub = open('jobs.sub', 'w')
    exec_base = 'executable    = /afs/cern.ch/user/o/ocerri/cernbox/BPhysics/MCGeneration/BPH_CMSMCGen/'
    if args.PU == 0:
        fsub.write(exec_base+'job1023_gen_NoPU_v1.sh')
    elif isinstance(args.PU, int) and args.PU > 0:
        fsub.write(exec_base+'job1023_gen_wPU_v1.sh')
    fsub.write('\n')
    exec_args = str(nev)+' '+str(st_seed)+' $(ProcId) '+args.process+' '+version+' '+args.CMSSW_loc
    if isinstance(args.PU, int) and args.PU > 0:
        exec_args += ' ' + str(args.PU)
    fsub.write('arguments     = ' + exec_args)
    fsub.write('\n')
    fsub.write('output        = {}/out/{}.$(ClusterId).$(ProcId).out'.format(outdir, args.process))
    fsub.write('\n')
    fsub.write('error         = {}/out/{}.$(ClusterId).$(ProcId).err'.format(outdir, args.process))
    fsub.write('\n')
    fsub.write('log           = {}/out/{}.$(ClusterId).$(ProcId).log'.format(outdir, args.process))
    fsub.write('\n')
    fsub.write('+MaxRuntime   = '+str(maxRunTime))
    fsub.write('\n')
    # fsub.write('+JobBatchName = '+args.process)
    # fsub.write('\n')
    fsub.write('x509userproxy = $ENV(X509_USER_PROXY)')
    fsub.write('\n')
    fsub.write('queue '+str(njobs))
    fsub.write('\n')
    fsub.close()

    print 'Submitting jobs...'
    output = processCmd('condor_submit jobs.sub')
    print 'Jobs submitted'
    os.rename('jobs.sub', outdir+'/cfg/jobs.sub')
