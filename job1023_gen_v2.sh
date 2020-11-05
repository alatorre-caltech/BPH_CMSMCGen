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

evtContent="RAWSIM"
steps="GEN,SIM"
if [ "$N_PU" == "GENonly" ]
then
  evtContent="GENRAW"
  steps="GEN"
fi

cmsDriver.py Configuration/GenProduction/python/${process_name}_cfi.py --fileout file:${output_flag}_GEN-SIM.root --mc --eventcontent $evtContent --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v15 --beamspot Realistic25ns13TeVEarly2018Collision --step $steps --nThreads $N_Threads --geometry DB:Extended --era Run2_2018 --python_filename step1_${output_flag}_GEN-SIM_cfg.py --no_exec -n $N_evts

echo "process.RandomNumberGeneratorService.generator.initialSeed = $N_seed" >> step1_${output_flag}_GEN-SIM_cfg.py
echo "process.MessageLogger.cerr.FwkReport.reportEvery = 100" >> step1_${output_flag}_GEN-SIM_cfg.py

echo "--> Running step 1"
date
echo "--> Running step 1" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log
cmsRun step1_${output_flag}_GEN-SIM_cfg.py 2>&1 | tee step1.log
exitcode=$?

if [ "$N_PU" == "GENonly" ]
then
  cp ${output_flag}_GEN-SIM.root $out_dir/${output_flag}_GEN-SIM_${N_seed}.root

  cp ./*.log $out_dir/${output_flag}_${N_seed}/

  echo "Job finished"
  date
  echo "Job finished" >> ${output_flag}.log
  echo `date +%s.%N` >> ${output_flag}.log
  exit $exitcode
fi


echo "Step 2: GEN-SIM -> RAW"
date
echo "Step 2: GEN-SIM -> RAW" >> ${output_flag}.log
echo `date +%s.%N` >> ${output_flag}.log

if [ "$N_PU" == "0" ]
then
  echo "No pileup option"
  cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1
elif [[ "$N_PU" =~ ^[0-9]+$ ]]
then
  echo "Poisson pileup with average $N_PU"
  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': ${N_PU}}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"
elif [ "$N_PU" == "customTest" ]
then
  echo "Custom pileup: $N_PU"
  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': 30}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"

  sed -i "87iprocess.mix.input.nbPileupEvents = cms.PSet(probFunctionVariable=cms.vint32(0, 1, 2, 3, 4, 5, 6, 7, 8), probValue=cms.vdouble(0.16666666666666666, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0, 0.0, 0.0, 0.5), histoFileName=cms.untracked.string('histoPileupProbFunction.root'))" step2_${output_flag}_RAW_cfg.py
  # echo $str >> step2_${output_flag}_RAW_cfg.py
  sed -i "86d" step2_${output_flag}_RAW_cfg.py
elif [ "$N_PU" == "c0" ]
then
  echo "Custom pileup: $N_PU"
  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': 30}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"

  sed -i "87iprocess.mix.input.nbPileupEvents = cms.PSet(probFunctionVariable=cms.vint32(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79), probValue=cms.vdouble(0.00000, 0.00000, 0.00001, 0.00005, 0.00016, 0.00139, 0.00197, 0.00297, 0.00449, 0.00652, 0.00895, 0.01165, 0.01446, 0.01733, 0.02025, 0.02325, 0.02634, 0.02945, 0.03242, 0.03505, 0.03717, 0.03865, 0.03948, 0.03974, 0.03956, 0.03906, 0.03836, 0.03749, 0.03646, 0.03525, 0.03382, 0.03216, 0.03030, 0.02826, 0.02613, 0.02397, 0.02184, 0.01981, 0.01791, 0.01616, 0.01456, 0.01310, 0.01178, 0.01057, 0.00947, 0.00846, 0.00754, 0.00669, 0.00592, 0.00523, 0.00460, 0.00403, 0.00353, 0.00309, 0.00271, 0.00238, 0.00209, 0.00185, 0.00166, 0.00149, 0.00136, 0.00126, 0.00118, 0.00112, 0.00107, 0.00103, 0.00101, 0.00099, 0.00097, 0.00096, 0.00001, 0.00001, 0.00001, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000), histoFileName=cms.untracked.string('histoPileupProbFunction.root'))" step2_${output_flag}_RAW_cfg.py
  # echo $str >> step2_${output_flag}_RAW_cfg.py
  sed -i "86d" step2_${output_flag}_RAW_cfg.py
  sed -i "86iprocess.mix.input.type = cms.string('probFunction')" step2_${output_flag}_RAW_cfg.py
elif [ "$N_PU" == "c1" ]
then
  echo "Custom pileup: $N_PU"
  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': 30}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"

  sed -i "87iprocess.mix.input.nbPileupEvents = cms.PSet(probFunctionVariable=cms.vint32(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79), probValue=cms.vdouble(0.00000, 0.00000, 0.00000, 0.00001, 0.00005, 0.00108, 0.00128, 0.00167, 0.00230, 0.00325, 0.00452, 0.00610, 0.00797, 0.01010, 0.01248, 0.01511, 0.01795, 0.02093, 0.02391, 0.02670, 0.02914, 0.03109, 0.03253, 0.03350, 0.03413, 0.03455, 0.03491, 0.03525, 0.03558, 0.03582, 0.03587, 0.03563, 0.03499, 0.03394, 0.03248, 0.03069, 0.02866, 0.02652, 0.02435, 0.02226, 0.02029, 0.01849, 0.01686, 0.01538, 0.01405, 0.01282, 0.01169, 0.01064, 0.00965, 0.00872, 0.00784, 0.00702, 0.00626, 0.00556, 0.00491, 0.00433, 0.00381, 0.00335, 0.00294, 0.00259, 0.00228, 0.00202, 0.00181, 0.00162, 0.00147, 0.00135, 0.00126, 0.00118, 0.00112, 0.00107, 0.00009, 0.00007, 0.00005, 0.00003, 0.00002, 0.00001, 0.00001, 0.00001, 0.00000, 0.00000), histoFileName=cms.untracked.string('histoPileupProbFunction.root'))" step2_${output_flag}_RAW_cfg.py
  # echo $str >> step2_${output_flag}_RAW_cfg.py
  sed -i "86d" step2_${output_flag}_RAW_cfg.py
  sed -i "86iprocess.mix.input.type = cms.string('probFunction')" step2_${output_flag}_RAW_cfg.py
else
  echo "No recognized pileup information"
  exit
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
