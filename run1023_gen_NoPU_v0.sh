#!/bin/bash

# process_name=HardQCD_bbar_Bu_D0munu_KPimunu
# process_name=BPH_gammaTRIAL_Tag-Bm_D0kpmunu_Probe-Bp_D0kpmunu
# process_name=BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0kptaunu_tau2mununu
# process_name=BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0stkpNeumunu
# process_name=BPH_Tag-Bm_D0kpmunu_Probe-Bp_D0stkpNeutaunu_tau2mununu

process_name=BPH_Tag-Bm_D0kpmunu_Probe-B0_MuNuDmst-pD0bar-kp-
# process_name=BPH_Tag-Bm_D0kpmunu_Probe-B0_TauNuDmst-pD0bar-kp-tau2mununu

version=NoPU_10-2-3_v1
out_loc=/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private
N_evts=$1
# N_evts=100000

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
# cd /afs/cern.ch/user/o/ocerri/cernbox/BPhysics/CMSSW_10_2_3/src
cd /afs/cern.ch/user/o/ocerri/work/CMSSW_10_2_3/src/

eval `scramv1 runtime -sh`

# mkdir -p Configuration/GenProduction/python

cp $MC_frag_file Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py

scram b -j9

echo "cmsDriver.py Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py --fileout file:${process_name}_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v12 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2018 --python_filename step1_${process_name}_GEN-SIM_cfg.py --no_exec -n $N_evts"

cmsDriver.py Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py --fileout file:${process_name}_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v12 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2018 --python_filename step1_${process_name}_GEN-SIM_cfg.py --no_exec -n $N_evts
# --customise Configuration/DataProcessing/Utils.addMonitoring

echo "process.MessageLogger.cerr.FwkReport.reportEvery = 1000" >> step1_${process_name}_GEN-SIM_cfg.py


mv ./step1_${process_name}_GEN-SIM_cfg.py $out_dir/
mkdir -p $out_dir/Configuration/GenProduction/python
cp Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py $out_dir/Configuration/GenProduction/python/${process_name}_13TeV-pythia8-evtgen_cfi.py
# mv Configuration $out_dir/
cd $out_dir

cmsRun step1_${process_name}_GEN-SIM_cfg.py &> step1.log

exit

echo "Step 2: RAW -> MINIAOD"

cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v12 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 8 --era Run2_2018 --filein file:${process_name}_GEN-SIM.root --fileout file:${process_name}_RAW.root --python_filename step2_${process_name}_RAW_cfg.py --no_exec -n -1

cmsRun step2_${process_name}_RAW_cfg.py &> step2.log



cmsDriver.py --filein file:${process_name}_RAW.root --fileout file:${process_name}_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v12 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 8 --era Run2_2018 --python_filename step3_${process_name}_AODSIM_cfg.py --no_exec -n -1

cmsRun step3_${process_name}_AODSIM_cfg.py &> step3.log
rm ${process_name}_RAW.root



cmsDriver.py --filein file:${process_name}_AODSIM.root --fileout file:${process_name}_MINIAODSIM.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 102X_upgrade2018_realistic_v12 --step PAT --era Run2_2018 --nThreads 8 --python_filename step4_${process_name}_MINIAODSIM_cfg.py --no_exec -n -1

cmsRun step4_${process_name}_MINIAODSIM_cfg.py &> step4.log
rm ${process_name}_AODSIM.root
