#!/usr/bin/env python
import os, sys, subprocess, re
import argparse
import commands
import time
from glob import glob
#____________________________________________________________________________________________________________
### processing the external os commands
def processCmd(cmd, quite = 0):
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    return output

def compileCMSSW(CMSSW_loc):
    aux = raw_input('Do you want to compile CMSSW now? (y/n)\n')
    if 'y' in aux:
        print 'Now compiling ' + CMSSW_loc
        cmd = 'cd ' + CMSSW_loc
        cmd += '; source /cvmfs/cms.cern.ch/cmsset_default.sh'
        cmd += '; eval `scramv1 runtime -sh`'
        cmd += '; scram b -j12'
        os.system(cmd)
        return True
    else: return False

def createBatchName(a):
    knownTags = ['B0_JpsiKst', 'B0_Mu', 'B0_Tau']
    n = None
    for t in knownTags:
        if t in a.process:
            n = 'B' + t.split('_')[1]
    if n is None:
        n = 'jobs_' + a.maxtime
    else:
        n += '_{:.0f}k'.format(float(a.nev)/1000)
    return n

#_____________________________________________________________________________________________________________
processes = {
'mu'         : 'BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2',
'tau'        : 'BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2',
'Dstst'      : 'BPH_Tag-Bp_MuNuDstst_DmstPi_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2',
'KDst'       : 'BPH_Tag-Mu_Probe-B0_KDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVS',
'JpsiKst'    : 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVV',
'JpsiKstFSR' : 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgenFSR_SVV'
}
#_____________________________________________________________________________________________________________

#_____________________________________________________________________________________________________________
#example line: ./submitCondorJobs.py mu --nev 50000 --njobs 100 -f --PU 20
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument ('tag', type=str, choices=processes.keys(), help='Process tag')

    parser.add_argument ('--nev', help='number of events per job', default=1000)
    parser.add_argument ('--njobs', help='number of jobs', default=10)
    parser.add_argument ('--st_seed', help='starting seed', default=1, type=int)
    parser.add_argument ('--PU', help='PU collisions to be generated', default=0, type=int)

    parser.add_argument ('--version', help='Process version', default='')
    parser.add_argument ('--CMSSW_loc', help='CMSSW src loc', default=None)
    parser.add_argument ('--outdir', help='output directory ', default=None)
    parser.add_argument ('-f', '--force_production', action='store_true', default=False, help='Proceed even if the directory is already existing')
    parser.add_argument ('--notNice', action='store_true', default=False, help='Run nice jobs')
    parser.add_argument ('--jobsTag', help='Tag appended at the end of the output folder', default='')

    parser.add_argument ('--maxtime', help='Max wall run time [s=seconds, m=minutes, h=hours, d=days]', default='4h')
    parser.add_argument ('--memory', help='min virtual memory in MB', default='3000')
    parser.add_argument ('--disk', help='min disk space in KB', default='2000000')
    parser.add_argument ('--cpu', help='cpu threads', default='2')

    args = parser.parse_args()
    args.process = processes[args.tag]

    if args.CMSSW_loc is None:
        if os.uname()[1] == 'login-1.hep.caltech.edu':
            args.CMSSW_loc = '/storage/user/ocerri/generation/CMSSW_10_2_3/src'
        elif os.uname()[1][:6] == 'lxplus':
            args.CMSSW_loc = '/afs/cern.ch/user/o/ocerri/work/generation_CMSSW/CMSSW_10_2_3/src'
        else:
            print 'No default CMSSW location is set for', os.uname()[1]
            exit()

    if args.outdir is None:
        if os.uname()[1] == 'login-1.hep.caltech.edu':
            args.outdir = '/storage/user/ocerri/BPhysics/data/cmsMC_private'
        elif os.uname()[1][:6] == 'lxplus':
            args.outdir = '/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private'
        else:
            print 'No default output direcotry is set for', os.uname()[1]
            exit()

    nev        = args.nev
    njobs      = int(args.njobs)
    st_seed    = int(args.st_seed)
    cmssw_version = re.search('/CMSSW_[0-9]+_[0-9]+_[0-9]+/src', args.CMSSW_loc).group(0)[7:-4]
    version    = cmssw_version.replace('_', '-')
    if args.version:
        version += '_' + args.version

    outdir     = args.outdir+'/'+args.process+'_PU'+str(args.PU)+'_'+version+'/jobs_out'
    if args.jobsTag:
        outdir += '_' + args.jobsTag

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
        print 'Pre-existing MC fragment not found. Copying it from Configuration/GenProduction/python/'
        cmd = 'cp '
        cmd += 'Configuration/GenProduction/python/'
        cmd += mc_frag_name
        cmd += ' '+mc_frag_dir+'/'
        os.system(cmd)
        compileCMSSW(args.CMSSW_loc)
        print 'Re-run please.'
        sys.exit()
    else:
        print '--->> I hope you already compiled '+args.CMSSW_loc
        aux = raw_input('Have you? (y/n)\n')
        if 'n' in aux:
            compileCMSSW(args.CMSSW_loc)
            print 'Re-run please.'
            sys.exit()

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        os.makedirs(outdir+'/out/')
        os.makedirs(outdir+'/cfg/')
    elif not args.force_production:
        print 'Output dir: "'+outdir+'" exists.'
        aux = raw_input('Continue anyway? (y/n)\n')
        if aux == 'n':
            exit()

    existing_files = glob(outdir + '/out_MINIAODSIM_*.root')
    n_max = None
    for f in existing_files:
        f = os.path.basename(f).replace('.root', '')
        f = f.replace('out_MINIAODSIM_', '')
        f = int(f)
        if n_max is None or f > n_max:
            n_max = f
    if not n_max is None and args.st_seed <= n_max:
        print 'Max seed already present:', n_max
        print 'Starting seed set:', args.st_seed
        aux = raw_input('Do you want to raise the starting seed to {}? (y/n)\n'.format(n_max+1))
        if aux == 'y':
            st_seed = n_max + 1
            args.st_seed = n_max + 1

    os.system('chmod +x job1023_gen_v1.sh')
    print 'Creating submission script'

    fsub = open('jobs.jdl', 'w')
    fsub.write('executable    = ' + os.environ['PWD'] + '/job1023_gen_v1.sh')
    fsub.write('\n')
    exec_args = str(nev)+' '+str(st_seed)+' $(ProcId) '+args.process+' '+outdir+' '+args.CMSSW_loc+' '+str(args.PU)+' '+str(args.cpu)
    fsub.write('arguments     = ' + exec_args)
    fsub.write('\n')
    fsub.write('output        = {}/out/job_$(ProcId)_$(ClusterId).out'.format(outdir))
    fsub.write('\n')
    fsub.write('error         = {}/out/job_$(ProcId)_$(ClusterId).err'.format(outdir))
    fsub.write('\n')
    fsub.write('log           = {}/out/job_$(ProcId)_$(ClusterId).log'.format(outdir))
    fsub.write('\n')
    fsub.write('JobPrio = -1')
    fsub.write('\n')
    fsub.write('WHEN_TO_TRANSFER_OUTPUT = ON_EXIT_OR_EVICT')
    fsub.write('\n')
    fsub.write('+MaxRuntime   = '+str(maxRunTime))
    fsub.write('\n')
    if not args.notNice:
        fsub.write('nice_user = True\n')
    if os.uname()[1] == 'login-1.hep.caltech.edu':
        fsub.write('+RunAsOwner = True')
        fsub.write('\n')
        fsub.write('+InteractiveUser = True')
        fsub.write('\n')
        fsub.write('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/bbockelm/cms:rhel7"')
        fsub.write('\n')
        fsub.write('+SingularityBindCVMFS = True')
        fsub.write('\n')
        fsub.write('run_as_owner = True')
        fsub.write('\n')
        fsub.write('RequestDisk = ' + args.disk)
        fsub.write('\n')
        fsub.write('RequestMemory = ' + args.memory) #Static allocation
        # fsub.write('RequestMemory = ifthenelse(MemoryUsage =!= undefined, MAX({{MemoryUsage + 1024, {0}}}), {0})'.format(args.memory)) # Dynamic allocation
        fsub.write('\n')
        fsub.write('RequestCpus = ' + str(args.cpu))
        fsub.write('\n')
    fsub.write('x509userproxy = $ENV(X509_USER_PROXY)')
    fsub.write('\n')
    fsub.write('on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)')
    fsub.write('\n')
    fsub.write('on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)')   # Send the job to Held state on failure.
    fsub.write('\n')
    if args.notNice:
        fsub.write('periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*20))')   # Periodically retry the jobs for 3 times with an interval of 20 minutes.
        fsub.write('\n')
    fsub.write('+PeriodicRemove = ((JobStatus =?= 2) && ((MemoryUsage =!= UNDEFINED && MemoryUsage > 2.5*RequestMemory)))')
    fsub.write('\n')
    fsub.write('max_retries    = 3')
    fsub.write('\n')
    fsub.write('requirements   = Machine =!= LastRemoteHost && TARGET.Machine != "blade-1.tier2"')
    fsub.write('\n')
    fsub.write('universe = vanilla')
    fsub.write('\n')
    fsub.write('queue '+str(njobs))
    fsub.write('\n')
    fsub.close()

    #Create tmp directory
    if not os.path.isdir('tmp_return'):
        os.system('mkdir tmp_return')
    os.system('mv jobs.jdl tmp_return/jobs.jdl')

    print 'Submitting jobs...'
    cmd = 'cd tmp_return; condor_submit jobs.jdl'
    cmd += ' -batch-name ' + createBatchName(args)
    output = processCmd(cmd)
    print 'Jobs submitted'
    os.rename('tmp_return/jobs.jdl', outdir+'/cfg/jobs.jdl')
    call = '"' + ' '.join(sys.argv)
    call += '; starting seed: ' + str(args.st_seed)
    call += '"'
    cmd = 'echo ' + call + ' >> ' + outdir+'/cfg/call.log'
    os.system(cmd)
    os.system('cd ..')
