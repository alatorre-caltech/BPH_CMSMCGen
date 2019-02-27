#!/usr/bin/env python
import os, sys, subprocess
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
#example line: python submitCondorJobs.py --nev 30000 --njobs 100 --maxtime 1h
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument ('--nev', help='number of events per job', default=100)
    parser.add_argument ('--njobs', help='number of jobs', default=10)
    parser.add_argument ('--st_seed', help='starting seed', default=1, type=int)

    parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-B0_MuNuDmst-pD0bar-kp-')

    parser.add_argument ('--version', help='Process version', default='NoPU_10-2-3_v0')
    parser.add_argument ('--CMSSW_loc', help='CMSSW src loc', default='/afs/cern.ch/user/o/ocerri/work/CMSSW_10_2_3/src')
    parser.add_argument ('--outdir', help='output directory ', default='/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private')
    parser.add_argument ('--force_production', action='store_true', default=False, help='Proceed even if the directory is already existing')
    parser.add_argument ('--maxtime', help='Max wall run time [s=seconds, m=minutes, h=hours, d=days]', default='8h')
    # parser.add_argument ('--memory', help='min virtual memory', default='8000')
    # parser.add_argument ('--disk', help='min disk space', default='8000')

    args = parser.parse_args()

    nev        = args.nev
    njobs      = int(args.njobs)
    st_seed    = int(args.st_seed)

    outdir     = args.outdir + '/' + args.process + '_' + args.version + '/jobs_out'

    time_scale = {'s':1, 'm':60, 'h':60*60, 'd':60*60*24}
    maxRunTime = int(args.maxtime[:-1]) * time_scale[args.maxtime[-1]]
    # mem       = args.memory
    # disk      = args.disk

    mc_frag_dir = args.CMSSW_loc+'/Configuration/GenProduction/python'
    if not os.path.exists(mc_frag_dir):
        os.makedirs(mc_frag_dir)

    mc_frag_name = args.process+'_13TeV-pythia8-evtgen_cfi.py'
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
        aux = raw_input('Have you? (y/n) ')
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
    print 'Creating submission script\n\n'

    fsub = open('jobs.sub', 'w')
    fsub.write('executable    = /afs/cern.ch/user/o/ocerri/cernbox/BPhysics/MCGeneration/BPH_CMSMCGen/job1023_gen_NoPU_v1.sh')
    fsub.write('\n')
    fsub.write('arguments     = '+str(nev)+' '+str(st_seed)+' $(ProcId) '+args.process+' '+args.version+' '+args.CMSSW_loc)
    fsub.write('\n')
    fsub.write('output        = {}/out/{}.$(ClusterId).$(ProcId).out'.format(outdir, args.process))
    fsub.write('\n')
    fsub.write('error         = {}/out/{}.$(ClusterId).$(ProcId).err'.format(outdir, args.process))
    fsub.write('\n')
    fsub.write('log           = {}/out/{}.$(ClusterId).$(ProcId).log'.format(outdir, args.process))
    fsub.write('\n')
    fsub.write('+MaxRuntime   = '+str(maxRunTime))
    fsub.write('\n')
    fsub.write('queue '+str(njobs))
    fsub.close()

    # output = processCmd('condor_submit jobs.sub')
    os.rename('jobs.sub', outdir+'/cfg/jobs.sub')
