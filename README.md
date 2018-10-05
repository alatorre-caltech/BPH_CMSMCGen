# BPH_GenConfigurations
List of already produced samples available here
https://docs.google.com/spreadsheets/d/1gCBiTc4z8wgsmn-PpmI22gYUlcBTETjwJZ8cir5t7gk/edit#gid=0

# Steps to generate files
Step 0: gen fragment

Any MC process should be described in a so-called gen fragment
Ozlem Ozludil (BPH MC contact) has kindly provided the following one for
B0 ->  mu- D*+;  D*+->D0 pi+; D0->K- pi+  and plus the bachelor muon also w/o cuts from the tag side
https://github.com/oozcelik/Fragments/blob/master/B0ToDstarMu_13TeV-pythia8-evtgen_cfi.py

In previous generation campaigns with muons on both sides of the event, the following filter has also been used

muPtFilter = cms.EDFilter("PythiaFilter",  # bachelor muon with kinematic cuts.
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(5.), #used to be 7 GeV
    ParticleID = cms.untracked.int32(13),
)

Nothing prevents this requirement to be applied on the probe side, so only events where it is explicitly required that the muon from the tag side has pT>5 GeV should be considered at analysis level.
If this filter is to be used, it should be added to the ProductionFilterSequence


Step 1: GEN-SIM

cmsrel CMSSW_9_3_6
cd CMSSW_9_3_6/src
cmsenv
mkdir -p Configuration/GenProduction/python
#put the gen fragment in this directory
cd -
scram b -j 9

cmsDriver.py Configuration/GenProduction/python/Bu_D0munu_KPimunu_13TeV-pythia8-evtgen_cfi.py --fileout file:BuToD0MuNu_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --nThreads 1 --geometry DB:Extended --era Run2_2017 --python_filename step1_BuToD0MuNu_GEN-SIM_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 50

Step 2: PU Mixing + RAW

cmsrel CMSSW_9_4_4
cd CMSSW_9_4_4/src
cmsenv
scram b -j 9

cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v12 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --nThreads 4 --datamix PreMix --era Run2_2017 --filein file:../../CMSSW_9_3_6/src/BuToD0MuNu_GEN-SIM.root --fileout file:BuToD0MuNu_PUMix.root --python_filename step2_BuToD0MuNu_PUMix_cfg.py --pileup_input /store/mc/RunIISummer17PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MC_v2_94X_mc2017_realistic_v9-v1/30042/C849424C-EDD3-E711-A63D-001E67E6F922.root --no_exec -n -1


Step 3: AODSIM
(in 9_4_4 as well)

cmsDriver.py --filein file:BuToD0MuNu_PUMix.root --fileout file:BuToD0MuNu_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v12 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 4 --era Run2_2017 --python_filename step3_BuToD0MuNu_AODSIM_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

Step 4: MINIAODSIM
(in 9_4_4 as well)

cmsDriver.py --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 94X_mc2017_realistic_v12 --step PAT --era Run2_2017 --filein file:BuToD0MuNu_AODSIM.root --fileout file:BuToD0MuNu_MINIAODSIM.root --python_filename step4_BuToD0MuNu_MINIAODSIM_cfg.py --no_exec -n -1
