# Run with: crab submit -c crab_config.py
import os
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

N_PU = 20
st_seed = 1801
njobs = 3500

################## Define the process name here only once ######################
# maxtime = '10h'
# process_name = 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVV'
# nev = 300000

# maxtime = '10h'
# process_name = 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_SVV'
# nev = 50000

# maxtime = '10h'
# process_name = 'BPH_Tag-B0_DmstHc-pD0bar-kp-Hc2mu_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen'
# nev = 400000

maxtime = '10h'
process_name = 'BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
nev = 300000

# maxtime = '12h'
# process_name = 'BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
# nev = 150000

################################################################################

import datetime
currentDT = str(datetime.datetime.now())
str2tail = '  '.join([currentDT, process_name, 'st_seed='+str(st_seed), 'n_ev='+str(nev), 'n_jobs='+str(njobs), 'maxtime='+str(maxtime), 'PU='+str(N_PU)])
os.system('echo "{}" >> generationLog.txt'.format(str2tail))

time_scale = {'m':1, 'h':60, 'd':60*24}

config = config()

config.General.requestName     = process_name + '_PU' + str(N_PU) + '_' + os.environ['CMSSW_VERSION'][6:].replace('_','-')
config.General.workArea        = 'tmp'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'placeholder_cfg.py'
#These files will be placed in the starting directory
config.JobType.inputFiles = ['Configuration/GenProduction/python/{}_cfi.py'.format(process_name), 'job1023_gen_v1.sh']
config.JobType.outputFiles = ['outlog.root', 'step1log.root', 'step2log.root', 'step3log.root', 'step4log.root']
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = int(maxtime[:-1]) * time_scale[maxtime[-1]]
config.JobType.scriptExe = 'crab_job.sh'
config.JobType.scriptArgs = ['nev='+str(nev), 'st_seed='+str(st_seed), 'process_name='+process_name, 'N_PU='+str(N_PU)]

config.Data.outputPrimaryDataset = 'cmsMC_private'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 10 #placeholder
config.Data.totalUnits           = njobs * config.Data.unitsPerJob
config.Data.publication          = True
config.Data.outputDatasetTag     = process_name + '_PU' + str(N_PU) + '_' + os.environ['CMSSW_VERSION'][6:].replace('_','-')

config.Site.storageSite = 'T2_US_Caltech'
config.Site.blacklist = ['T2_EE_*']
