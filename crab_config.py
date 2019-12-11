# Run with: crab submit -c crab_config.py
import os
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import datetime

N_Threads = 2
N_PU = 20
st_seed = 5001
njobs = 10000

################## Define the process name here only once ######################
# maxtime = '12h'
# process_name = 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVV'
# nev = 300000

# maxtime = '10h'
# process_name = 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_SVV'
# nev = 50000

# maxtime = '12h'
# process_name = 'BPH_Tag-B0_DmstHc-pD0bar-kp-Hc2mu_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen'
# nev = 300000

# maxtime = '12h'
# process_name = 'BPH_Tag-Bp_MuNuDstst_DmstPi_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
# nev = 100000

# maxtime = '14h'
# process_name = 'BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
# process_name = 'BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_HQET2_central'
# nev = 200000

maxtime = '15h'
process_name = 'BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
nev = 100000
################################################################################

time_scale = {'m':1, 'h':60, 'd':60*24}

config = config()

currentDT = str(datetime.datetime.now())
shortDate = currentDT[2:].split(' ')[0].replace('-','')
config.General.requestName     = process_name + '_PU' + '_'.join([str(N_PU), os.environ['CMSSW_VERSION'][6:].replace('_','-'), shortDate])
config.General.workArea        = 'tmp'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'placeholder_cfg.py'
#These files will be placed in the starting directory
config.JobType.inputFiles = ['Configuration/GenProduction/python/{}_cfi.py'.format(process_name), 'job1023_gen_v1.sh']
# config.JobType.outputFiles = ['outlog.root', 'step1log.root', 'step2log.root', 'step3log.root', 'step4log.root']
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 4000
config.JobType.numCores = N_Threads
config.JobType.maxJobRuntimeMin = int(maxtime[:-1]) * time_scale[maxtime[-1]]
config.JobType.scriptExe = 'crab_job.sh'
config.JobType.scriptArgs = ['nev='+str(nev), 'st_seed='+str(st_seed), 'process_name='+process_name, 'N_PU='+str(N_PU), 'N_Threads='+str(N_Threads)]

config.Data.outputPrimaryDataset = 'cmsMC_private_PU' + str(N_PU) + '_' + os.environ['CMSSW_VERSION'][6:].replace('_','-')
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 10 #placeholder
config.Data.totalUnits           = njobs * config.Data.unitsPerJob
config.Data.publication          = True
config.Data.outputDatasetTag     = process_name + '_' + shortDate

config.Site.storageSite = 'T2_US_Caltech'
config.Site.blacklist = ['T2_EE_*']
if N_PU > 0:
    if not os.path.isfile('sitesWithPileupDataset.txt'):
        raise
    list = []
    with open('sitesWithPileupDataset.txt') as file:
        for ln in file.readlines():
            ln = ln[:-1]
            if ln[:2]=='T0' or ln[:2]=='T1': continue
            list.append(ln)
    config.Site.whitelist = list

str2tail = '  '.join([currentDT, process_name, 'st_seed='+str(st_seed), 'n_ev='+str(nev), 'n_jobs='+str(njobs), 'maxtime='+str(maxtime), 'PU='+str(N_PU)])
os.system('echo "{}" >> generationLog.txt'.format(str2tail))
