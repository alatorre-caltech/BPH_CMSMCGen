#!/bin/bash
set -e
#Meant to run with HTCondor

#This job does not compile the CMSSW with the fragments. Be mindful and compile it haead.

N_evts=$1
echo "N_evts=$N_evts"
st_seed=$2
echo "st_seed=$st_seed"
proc_ID=$3
echo "proc_ID=$proc_ID"
process_name=$4
echo "process_name=$process_name"
out_dir=$5
echo "out_dir=$out_dir"
CMSSW_src_dir=$6
echo "CMSSW_src_dir=$CMSSW_src_dir"
N_PU=$7
echo "N_PU=$N_PU"
N_Threads=$8
echo "N_Threads=$N_Threads"

N_seed=$((st_seed+proc_ID))
echo "N_seed=$N_seed"
# out_loc=/eos/user/o/ocerri/BPhysics/data/cmsMC_private
# out_dir=$out_loc/${process_name}_PU${N_PU}_${version}/jobs_out/
output_flag=out

#Dump output locally
exec 2>&1 | tee ${output_flag}.log
echo "Starting job"
date
echo "Starting job" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log

if [ -d $out_dir/${output_flag}_${N_seed} ]
then
  rm -rf $out_dir/${output_flag}_${N_seed}
fi
mkdir $out_dir/${output_flag}_${N_seed}

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $CMSSW_src_dir
eval `scramv1 runtime -sh`
cd -

echo "Step 1: GEN-SIM"
date
echo "Step 1: GEN-SIM" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsDriver.py Configuration/GenProduction/python/${process_name}_cfi.py --fileout file:${output_flag}_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v15 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads $N_Threads --geometry DB:Extended --era Run2_2018 --python_filename step1_${output_flag}_GEN-SIM_cfg.py --no_exec -n $N_evts

echo "process.RandomNumberGeneratorService.generator.initialSeed = $N_seed" >> step1_${output_flag}_GEN-SIM_cfg.py
echo "process.MessageLogger.cerr.FwkReport.reportEvery = 50" >> step1_${output_flag}_GEN-SIM_cfg.py

echo "--> Running step 1"
date
echo "--> Running step 1" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsRun step1_${output_flag}_GEN-SIM_cfg.py 2>&1 | tee step1.log


echo "Step 2: GEN-SIM -> RAW"
date
echo "Step 2: GEN-SIM -> RAW" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log

if [ $N_PU -gt 0 ]
then
  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads $N_Threads --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': ${N_PU}}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"
#--pileup_input filelist:/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/MCGeneration/BPH_CMSMCGen/PU_file_list/MinBias_TuneCP5_13TeV-pythia8__RunIIFall18GS-102X_upgrade2018_realistic_v9-v1__GEN-SIM.txt
else
  cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads $N_Threads --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1
fi

echo "--> Running step 2"
date
echo "--> Running step 2" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsRun step2_${output_flag}_RAW_cfg.py 2>&1 | tee step2.log


echo "Step 3: RAW -> AOD"
date
echo "Step 3: RAW -> AOD" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsDriver.py --filein file:${output_flag}_RAW.root --fileout file:${output_flag}_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads $N_Threads --era Run2_2018 --python_filename step3_${output_flag}_AODSIM_cfg.py --no_exec -n -1

echo "--> Running step 3"
date
echo "--> Running step 3" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsRun step3_${output_flag}_AODSIM_cfg.py 2>&1 | tee step3.log


echo "Step 4: AOD -> MINIAOD"
date
echo "Step 4: AOD -> MINIAOD" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsDriver.py --filein file:${output_flag}_AODSIM.root --fileout file:${output_flag}_MINIAODSIM.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 102X_upgrade2018_realistic_v15 --step PAT --era Run2_2018 --nThreads $N_Threads --python_filename step4_${output_flag}_MINIAODSIM_cfg.py --no_exec -n -1

echo "--> Running step 4"
date
echo "--> Running step 4" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsRun step4_${output_flag}_MINIAODSIM_cfg.py 2>&1 | tee step4.log
exitcode=$?
echo "CMSSW step4 exit code: $exitcode"
echo "Generation done"
date
echo "Generation done" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log

cp ${output_flag}_MINIAODSIM.root $out_dir/${output_flag}_MINIAODSIM_${N_seed}.root

cp ./*.log $out_dir/${output_flag}_${N_seed}/

echo "Job finished"
date
echo "Job finished" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
exit $exitcode
# rm ./step*.py
# rm ./*.log
# rm ./*.root
