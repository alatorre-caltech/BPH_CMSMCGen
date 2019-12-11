# BPH MC generation with CMS software

This repo contains the MC fragments and the scripts necessary to run a MC generation in CMSSW.

### Pile-up file list
To generate the PU file list from das use the following command:
``das_client --query="file dataset = /MinBias_TuneCP5_13TeV-pythia8/<..>/GEN-SIM" --limit=0 >> file.txt``

### Pile-up presence list
dasgoclient --query="site dataset=/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM" > sitesWithPileupDataset.txt
