#!/bin/bash
#Meant to run with HTCondor

N_evts=$1
st_seed=$2
proc_ID=$3
process_name=$4
version=$5
CMSSW_src_dir=$6
N_PU=$7

N_seed=$((st_seed+proc_ID))
out_loc=/eos/user/o/ocerri/BPhysics/data/cmsMC_private
out_dir=$out_loc/${process_name}_${version}/jobs_out/



# CMSSW_src_dir=/afs/cern.ch/user/o/ocerri/work/CMSSW_10_2_3/src
cd $CMSSW_src_dir
eval `scramv1 runtime -sh`
cd -


cmsDriver.py Configuration/GenProduction/python/${process_name}_cfi.py --fileout file:${process_name}_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v15 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2018 --python_filename step1_${process_name}_GEN-SIM_cfg.py --no_exec -n $N_evts

echo "process.RandomNumberGeneratorService.generator.initialSeed = $N_seed" >> step1_${process_name}_GEN-SIM_cfg.py
echo "process.MessageLogger.cerr.FwkReport.reportEvery = 50" >> step1_${process_name}_GEN-SIM_cfg.py
cmsRun step1_${process_name}_GEN-SIM_cfg.py



cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 8 --era Run2_2018 --filein file:${process_name}_GEN-SIM.root --fileout file:${process_name}_RAW.root --python_filename step2_${process_name}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': ${N_PU}}" --pileup_input filelist:/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/MCGeneration/BPH_CMSMCGen/PU_file_list/MinBias_TuneCP5_13TeV-pythia8__RunIIFall18GS-102X_upgrade2018_realistic_v9-v1__GEN-SIM.txt
# --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"

cmsRun step2_${process_name}_RAW_cfg.py



cmsDriver.py --filein file:${process_name}_RAW.root --fileout file:${process_name}_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 8 --era Run2_2018 --python_filename step3_${process_name}_AODSIM_cfg.py --no_exec -n -1

cmsRun step3_${process_name}_AODSIM_cfg.py



cmsDriver.py --filein file:${process_name}_AODSIM.root --fileout file:${process_name}_MINIAODSIM.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 102X_upgrade2018_realistic_v15 --step PAT --era Run2_2018 --nThreads 4 --python_filename step4_${process_name}_MINIAODSIM_cfg.py --no_exec -n -1

cmsRun step4_${process_name}_MINIAODSIM_cfg.py

cp ${process_name}_MINIAODSIM.root $out_dir/${process_name}_MINIAODSIM_${N_seed}.root

rm ./step*.py
rm ./*.root
