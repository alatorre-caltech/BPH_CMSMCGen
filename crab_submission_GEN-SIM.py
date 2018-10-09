from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName     = 'HardQCD_bbar_Bu_D0munu_KPimunu_GEN-SIM_18_10_08'
config.General.workArea        = 'HardQCD_bbar_Bu_D0munu_KPimunu'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'step1_HardQCD_bbar_Bu_D0munu_KPimunu_GEN-SIM_cfg.py'
config.JobType.numCores = 1

config.Data.outputPrimaryDataset = 'HardQCD_bbar_Bu_D0munu_KPimunu_Pythia'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 10000
config.Data.totalUnits           = 1500000
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = 'HardQCD_bbar_Bu_D0munu_KPimunu_GEN-SIM_18_10_08'

config.Site.storageSite = 'T2_US_Caltech'
