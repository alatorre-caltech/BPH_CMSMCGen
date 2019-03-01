from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName     = 'HardQCD_bbar_Bu_D0munu_KPimunu_GEN-SIM_18_10_09'
config.General.workArea        = 'BPhysics_gen'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName   = 'step1_HardQCD_bbar_Bu_D0munu_KPimunu_GEN-SIM_cfg.py'
config.JobType.numCores = 2

config.Data.outputPrimaryDataset = 'BPhysics'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'EventBased'
config.Data.unitsPerJob          = 500
config.Data.totalUnits           = 50
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = 'HardQCD_bbar_Bu_D0munu_KPimunu_GEN-SIM_18_10_09'

config.Site.storageSite = 'T2_CH_CERN'
