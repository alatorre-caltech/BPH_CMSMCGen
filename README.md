# BPH MC generation with CMS software

This repo contains the MC fragments and the scripts necessary to run a MC generation in CMSSW.

### Pile-up file list
To generate the PU file list from das use the following command:
``das_client --query="file dataset = /MinBias_TuneCP5_13TeV-pythia8/<..>/GEN-SIM" --limit=0 >> file.txt``
