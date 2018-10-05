from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName     = 'BToKmm_GEN-SIM_18_03_20'
config.General.workArea        = 'BToKmm'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'step1_BToKmm_GEN-SIM_cfg.py'
config.JobType.eventsPerLumi = 5000
config.JobType.numCores = 1

config.Data.outputPrimaryDataset = 'BToKmm_Pythia'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 500000
config.Data.totalUnits           = 5000000000
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = 'BToKmm_Pythia_GEN-SIM_18_03_20'

config.Site.storageSite = 'T2_UK_London_IC'
