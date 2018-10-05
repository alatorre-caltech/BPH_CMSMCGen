#!/bin/bash

process_name=Bu_D0munu_KPimunu
version=NoPU_9-4-4_v1
out_loc=/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private
N_evts=10000

out_dir=$out_loc/${process_name}_$version
MC_frag_file=/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/MCGeneration/BPH_CMSMCGen/Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py

if [ ! -d "$out_dir" ]; then
  echo "Creating the output directory"
  echo $out_dir
  mkdir $out_dir
else
  echo $out_dir
  echo "Directory already existing"
  read -p $'Do you want to delete it, recreate it and proceed? (y/n)\n' asw
  if [ asw="y" ];then
    rm -rfv $out_dir
    echo "Creating the output directory"
    echo $out_dir
    mkdir $out_dir
  else
    exit
  fi
fi

echo "Step 1: GEN-SIM"
cd /afs/cern.ch/user/o/ocerri/work/BPHGeneration/CMSSW_9_3_6/src
# cmsenv
eval `scramv1 runtime -sh`

mkdir -p Configuration/GenProduction/python

cp $MC_frag_file Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py

scram b -j9

cmsDriver.py Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py --fileout file:${process_name}_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --nThreads 4 --geometry DB:Extended --era Run2_2017 --python_filename step1_${process_name}_GEN-SIM_cfg.py --no_exec -n $N_evts
# --customise Configuration/DataProcessing/Utils.addMonitoring

mv ./* $out_dir/
cd $out_dir

cmsRun step1_${process_name}_GEN-SIM_cfg.py &> step1.log




echo "Step 2: RAW -> MINIAOD"

cd /afs/cern.ch/user/o/ocerri/work/BPHGeneration/CMSSW_9_4_4/src
# cmsenv
eval `scramv1 runtime -sh`

cd $out_dir

cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v12 --step DIGI,L1,DIGI2RAW,HLT:2e34v40 --nThreads 4 --era Run2_2017 --filein file:${process_name}_GEN-SIM.root --fileout file:${process_name}_RAW.root --python_filename step2_${process_name}_RAW_cfg.py --no_exec -n -1

cmsRun step2_${process_name}_RAW_cfg.py

cmsDriver.py --filein file:${process_name}_RAW.root --fileout file:${process_name}_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v12 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 4 --era Run2_2017 --python_filename step3_${process_name}_AODSIM_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1

cmsRun step3_${process_name}_AODSIM_cfg.py

cmsDriver.py --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 94X_mc2017_realistic_v12 --step PAT --era Run2_2017 --filein file:${process_name}_AODSIM.root --fileout file:${process_name}_MINIAODSIM.root --python_filename step4_${process_name}_MINIAODSIM_cfg.py --no_exec -n -1

cmsRun step4_${process_name}_MINIAODSIM_cfg.py
