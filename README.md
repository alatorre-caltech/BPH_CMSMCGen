# BPH MC generation with CMS software

This repo contains the MC fragments and the scripts necessary to run a MC generation in CMSSW.

### Pile-up file list
To generate the PU file list from das use the following command:
``das_client --query="file dataset = /MinBias_TuneCP5_13TeV-pythia8/<..>/GEN-SIM" --limit=0 >> file.txt``

### Pile-up presence list
dasgoclient --query="site dataset=/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM" > sitesWithPileupDataset.txt

### Check time and size for central request

``cmsDriver.py Configuration/GenProduction/python/BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2_cfi.py --fileout file:test_output.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v15 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 1 --geometry DB:Extended --era Run2_2018 --python_filename test_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10000 || exit $?``
``echo "process.MessageLogger.cerr.FwkReport.reportEvery = 100" >> test_cfg.py``
``cmsRun -e -j test_rt.xml test_cfg.py || exit $?``

"AvgEventTime" part for time/event (sec).
"Timing-tstoragefile-write-totalMegabytes" divided by "TotalEvents" for size/event (mB). In McM corresponding fragment is kB.
