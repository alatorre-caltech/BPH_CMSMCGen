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
#example line: python submitBatchJobs.py --nev 30000 --njobs 100 --queue 1nd
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument ('--nev', help='number of events per job', default=100)
    parser.add_argument ('--njobs', help='number of jobs', default=10)
    parser.add_argument ('--st_seed', help='starting seed', default=1, type=int)


    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0kptaunu_tau2mununu')
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0kpmunu')

    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0stkpNeumunu')
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0stkpNeutaunu_tau2mununu')

    parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-B0_MuNuDmst-pD0bar-kp-')
    # parser.add_argument ('-P', '--process', help='Process name', default='BPH_Tag-Bm_D0kpmunu_Probe-B0_TauNuDmst-pD0bar-kp-tau2mununu')


    parser.add_argument ('--version', help='Process version', default='NoPU_10-2-3_v0')
    parser.add_argument ('--CMSSW_loc', help='CMSSW src loc', default='/afs/cern.ch/user/o/ocerri/work/CMSSW_10_2_3/src')
    parser.add_argument ('--outdir', help='output directory ', default='/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private')
    parser.add_argument ('--force_production', action='store_true', default=False, help='Proceed even if the directory is already existing')
    parser.add_argument ('--queue', help='lsf queue', default='8nh')
    parser.add_argument ('--memory', help='min virtual memory', default='8000')
    parser.add_argument ('--disk', help='min disk space', default='8000')

    args = parser.parse_args()

    nev       = args.nev
    njobs     = int(args.njobs)
    st_seed   = int(args.st_seed)

    outdir    = args.outdir + '/' + args.process + '_' + args.version + '/jobs_out'

    queue     = args.queue
    mem       = args.memory
    disk      = args.disk

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

    if not os.path.exists(outdir):
        os.makedirs(outdir)
        os.makedirs(outdir+'/std/')
        os.makedirs(outdir+'/cfg/')
    elif not args.force_production:
        print 'Output dir: "'+outdir+'" exists.'
        aux = raw_input('Continue anyway? (y/n)\n')
        if aux == 'n':
            exit()

    os.system('chmod +x job1023_gen_NoPU_v0.sh')
    print '[Submitting jobs]'
    jobCount=0
    for job in xrange(njobs):

        print 'Submitting job '+str(job+1)+' / '+str(njobs)
        job += st_seed
        seed=str(job)

        basename = args.process+'_{}'.format(seed)

        cmd = 'bsub -o '+outdir+'/std/'+basename +'.out -e '+outdir+'/std/'+basename +'.err -q '+queue
        cmd += ' -R "rusage[mem={}:pool={}]"'.format(mem,disk)
        cmd += ' -J {}'.format(basename)
        cmd += ' /afs/cern.ch/user/o/ocerri/cernbox/BPhysics/MCGeneration/BPH_CMSMCGen/job1023_gen_NoPU_v0.sh'
        cmd += ' '+str(nev)+' '+str(seed)+' '+args.process+' '+args.version+' '+args.CMSSW_loc

        print cmd

        # submitting jobs
        output = processCmd(cmd)
        kk = 0
        while (kk<5 and ('error' in output)):
            kk += 1
            time.sleep(1.0);
            output = processCmd(cmd)
            if ('error' not in output):
                print 'Submitted after retry - job '+str(jobCount+1)
            else:
                print output

        jobCount += 1
        time.sleep(0.01);

#_______________________________________________________________________________________
if __name__ == "__main__":
    main()
