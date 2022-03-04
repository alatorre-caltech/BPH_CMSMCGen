# Run with: crab submit -c crab_config.py
import os
from CRABClient.UserUtilities import config
import datetime

N_Threads = 1
njobs = 10000
N_PU = 'c2'

#----------------- Background samples -----------------

## B(s) -> D** mu nu

st_seed = 20001
maxtime = '18h'
# process_name = 'BParking_Tag_Bd_MuNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2'
# process_name = 'BParking_Tag_Bd_MuNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2_v2'
process_name = 'BParking_Tag_Bd_MuNuDstPiPi_SoftQCDnonD_scale5_TuneCP5'
nev = 200000

# st_seed = 100000
# maxtime = '18h'
# # process_name = 'BParking_Tag_Bu_MuNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2'
# process_name = 'BParking_Tag_Bu_MuNuDstPiPi_SoftQCDnonD_scale5_TuneCP5'
# nev = 150000

# st_seed = 100000
# maxtime = '24h'
# process_name = 'BParking_Tag_Bd_TauNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2'
# nev = 150000

# st_seed = 200000
# maxtime = '18h'
# process_name = 'BParking_Tag_Bu_TauNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2'
# nev = 150000

# st_seed = 10001
# maxtime = '18h'
# process_name = 'BParking_Tag_Bu_DstDdX_SoftQCDnonD_scale5_TuneCP5'
# nev = 300000

## Others

# st_seed = 1
# maxtime = '12h'
# process_name = 'BParking_Tag_DstKu_KutoMu_SoftQCDnonD_scale5_TuneCP5'
# nev = 400000


#----------------- Anchillary samples -----------------
# st_seed = 10001
# maxtime = '14h'
# process_name = 'BParking_Bd_JpsiKst_SoftQCDnonD_scale5_TuneCP5_HELAMP'
# nev = 50000


time_scale = {'m':1, 'h':60, 'd':60*24}

config = config()

currentDT = str(datetime.datetime.now())
shortDate = currentDT[2:].split(' ')[0].replace('-','')
shortDate += '-' + currentDT.split(' ')[1].replace(':', '')[:4]

config.General.requestName     = process_name + '_PU' + '_'.join([str(N_PU), os.environ['CMSSW_VERSION'][6:].replace('_','-'), shortDate])
config.General.workArea        = 'tmp'
config.General.transferOutputs = True
# config.General.transferLogs    = True
config.General.transferLogs    = False

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'placeholder_cfg.py'
#These files will be placed in the starting directory
config.JobType.inputFiles = ['Configuration/GenProduction/python/{}_cfi.py'.format(process_name), 'job1023_gen_v2.sh', 'minBiasFilesList_211005.txt']
# config.JobType.outputFiles = ['outlog.root', 'step1log.root', 'step2log.root', 'step3log.root', 'step4log.root']
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 5000
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
# config.Site.blacklist = ['T2_EE_*']
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

str2tail = '  '.join([currentDT[:-7], process_name, 'st_seed='+str(st_seed), 'n_ev='+str(nev), 'n_jobs='+str(njobs), 'maxtime='+str(maxtime), 'PU='+str(N_PU)])
os.system('echo "{}" >> generationLog.txt'.format(str2tail))








################## OLD ######################
#----------------- JpsiKst -----------------
# maxtime = '12h'
# process_name = 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVV'
# nev = 300000

# maxtime = '10h'
# process_name = 'BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_SVV'
# nev = 50000

# st_seed = 30001
# maxtime = '24h'
# process_name = 'BP_Tag-Probe_B0_JpsiKst_Hardbbbar_evtgen_HELAMP'
# nev = 200000

# st_seed = 20001
# maxtime = '24h'
# process_name = 'BP_Tag-Probe_B0_JpsiKst_SoftQCD_evtgen_HELAMP'
# nev = 1000000

# st_seed = 10001
# maxtime = '20h'
# process_name = 'BP_Tag-Probe_Bp_JpsiK_Hardbbbar_evtgen_HELAMP'
# nev = 150000

#----------------- Old Tag -----------------
# st_seed = 72001
# maxtime = '15h'
# # process_name = 'BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
# process_name = 'BPH_Tag-B0_MuNuDmst_13TeV-pythia8_Hardbbbar_HQET2_central'
# nev = 150000

# st_seed = 0
# maxtime = '15h'
# process_name = 'BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
# nev = 100000

# st_seed = 20001
# maxtime = '12h'
# process_name = 'BPH_Tag-B0_DmstHc-pD0bar-kp-Hc2mu_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen'
# nev = 300000

# st_seed = 20001
# maxtime = '12h'
# process_name = 'BPH_Tag-Bp_MuNuDstst_DmstPi_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2'
# nev = 100000

#----------------- Tag -----------------
# st_seed = 100001
# maxtime = '20h'
# process_name = 'BP_Tag_B0_MuNuDmst_SoftQCDall_evtgen_ISGW2'
# nev = 3000000

# st_seed = 1
# maxtime = '16h'
# process_name = 'BP_Tag_antiB0_MuNuDmst_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 230001
# maxtime = '16h'
# process_name = 'BP_Tag_B0_MuNuDmst_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 50000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_TauNuDmst_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 60000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_DmstHc_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 80000
# maxtime = '12h'
# process_name = 'BP_Tag_Bp_MuNuDstst_Hardbbbar_evtgen_ISGW2'
# nev = 250000

# st_seed = 180000
# maxtime = '12h'
# process_name = 'BP_Tag_Bp_TauNuDstst_Pip_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Tag_B0_DmstPi0MuNu_Hardbbbar_evtgen_GR'
# nev = 200000

# st_seed = 30000
# maxtime = '12h'
# process_name = 'BP_Tag_Bp_MuNuDstst_PipPi0_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 10000
# maxtime = '12h'
# process_name = 'BP_Tag_Bp_MuNuDstPipPi0_Hardbbbar_evtgen_PHSP'
# nev = 300000

# st_seed = 80000
# maxtime = '16h'
# process_name = 'BP_Tag_B0_MuNuDstst_PipPim_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 50000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_MuNuDstPipPim_Hardbbbar_evtgen_PHSP'
# nev = 300000

# st_seed = 560000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_MuNuDstst_Pi0Pi0_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Tag_B0_MuNuDstst_Pi0_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 150000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_TauNuDstst_Pi0_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 3000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_MuNuDstPiPiPi_Hardbbbar_evtgen_PHSP'
# nev = 200000

# st_seed = 320000
# maxtime = '12h'
# process_name = 'BP_Tag_Bp_MuNuDstPiPiPi_Hardbbbar_evtgen_PHSP'
# nev = 200000

# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Tag_B0_DstmDsp_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 110000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_DstmD0_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 510000
# maxtime = '12h'
# process_name = 'BP_Tag_B0_DstmDp_Hardbbbar_evtgen_ISGW2'
# nev = 500000

# st_seed = 20001
# maxtime = '12h'
# process_name = 'BP_Tag_Bm_DstmHc_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# st_seed = 30000
# maxtime = '12h'
# process_name = 'BP_Tag_Bp_DstmHc_Hardbbbar_evtgen_ISGW2'
# nev = 500000

# st_seed = 60000
# maxtime = '12h'
# process_name = 'BP_Tag_antiB0_DstmHc_Hardbbbar_evtgen_ISGW2'
# nev = 300000

# N_PU = 'c1'
#----------------- Probe -----------------
# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Probe_B0_MuNuDmst_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Probe_B0_TauNuDmst_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2'
# nev = 200000
#
# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Probe_Bp_MuNuDstst_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2'
# nev = 200000
#
# st_seed = 0
# maxtime = '16h'
# process_name = 'BP_Probe_B0_DmstHc_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2'
# nev = 200000

# st_seed = 0
# maxtime = '12h'
# process_name = 'BP_Probe_B0_DmstPi_Tag-B_MuNuDst_Hardbbbar_evtgen'
# nev = 200000
################################################################################
