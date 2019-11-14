#!/bin/bash
set -e
# ------------------------------ SIGNAL -----------------------------------------
# process_name=BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central
# process_name=BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTHat5p0-evtgen_HQET2_central
# process_name=BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central
# process_name=BPH_Tag-Bp_MuNuD10-2420_DmstPi_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central
# process_name=BPH_NoCuts_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central
# process_name=BPH_NoCuts_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_SoftQCD_PTFilter5_0p0-evtgen_HQET2_central
# process_name=BPH_13TeV-pythia8_SoftQCD_PTFilter5_0p0
# process_name=BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2
# process_name=BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2
process_name=BPH_Tag-Bp_MuNuDstst_DmstPi_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2

ntuplizer_config=cmssw_privateMC_Tag_B0_MuDmst-pD0bar-kp.py
# --------------------------------------------------------------------------------

# ------------------------------ BACKGROUND -----------------------------------------
# process_name=BPH_Tag-B0_DmstHc-pD0bar-kp-Hc2mu_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen
# --------------------------------------------------------------------------------

# ------------------------------ CONTROL REGION ----------------------------------
# process_name=BPH_Tag-Mu_Probe-B0_KDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVS
# process_name=BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVV
# process_name=BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_SVV

# ntuplizer_config=cmssw_privateMC_Tag_Mu-Probe-B0_KDmst-pD0bar-kp.py
# ntuplizer_config=cmssw_privateMC_Tag_Mu-Probe-B0_JpsiKst-mumuKpi.py
# --------------------------------------------------------------------------------


output_flag=test

N_PU=20
version=PU${N_PU}_10-2-3
out_loc=/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private
if [ `uname -n` = "login-1.hep.caltech.edu" ]; then
  out_loc=/storage/user/ocerri/BPhysics/data/cmsMC_private
fi
N_evts=$1
# N_evts=100000

out_dir=$out_loc/${process_name}_$version
MC_frag_file=$PWD/Configuration/GenProduction/python/${process_name}_cfi.py

if [ ! -d "$out_dir" ]; then
  echo "Creating the output directory"
  echo $out_dir
  mkdir $out_dir
else
  echo $out_dir
  echo "Directory already existing, cleaning it"
  rm -fv $out_dir/test*
  rm -fv $out_dir/step*
  # read -p $'Do you want to delete it, recreate it and proceed? (y/n)\n' asw
  # if [ asw="y" ];then
  # echo "Creating the output directory"
  # echo $out_dir
  # mkdir $out_dir
  # else
  #   exit
  # fi
fi

#Save output
exec &> ${out_dir}/test.log

if [ `uname -n` = "login-1.hep.caltech.edu" ]; then
  cd /storage/user/ocerri/generation/test/CMSSW_10_2_3/src
else
  cd /afs/cern.ch/user/o/ocerri/work/generation_CMSSW/CMSSW_10_2_3/src/
fi
eval `scramv1 runtime -sh`

if [ ! -d "Configuration/GenProduction/python" ]; then
  mkdir -p Configuration/GenProduction/python
fi
cp $MC_frag_file Configuration/GenProduction/python/${process_name}_cfi.py

scram b -j12

echo "Starting job after compilation"
echo
echo "Step 1: GEN-SIM"
date
cmsDriver.py Configuration/GenProduction/python/${process_name}_cfi.py --fileout file:${output_flag}_GEN-SIM.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v15 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 2 --geometry DB:Extended --era Run2_2018 --python_filename step1_${output_flag}_GEN-SIM_cfg.py --no_exec -n $N_evts
# --customise Configuration/DataProcessing/Utils.addMonitoring

echo "process.RandomNumberGeneratorService.generator.initialSeed = 1" >> step1_${output_flag}_GEN-SIM_cfg.py
echo "process.MessageLogger.cerr.FwkReport.reportEvery = 100" >> step1_${output_flag}_GEN-SIM_cfg.py


mv ./step1_${output_flag}_GEN-SIM_cfg.py $out_dir/
mkdir -p $out_dir/Configuration/GenProduction/python
cp Configuration/GenProduction/python/${process_name}_cfi.py $out_dir/Configuration/GenProduction/python/${process_name}_cfi.py
# mv Configuration $out_dir/
cd $out_dir

echo "--> Running step 1"
date
cmsRun step1_${output_flag}_GEN-SIM_cfg.py &> step1.log

echo "Step 2: GEN-SIM -> RAW"
date

if [ $N_PU -gt 0]
then
  # Create PU file list
  # das_client --query="file dataset = /MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM" --limit=0 >> MinBias_TuneCP5_13TeV-pythia8_RunIIFall18GS-102X_upgrade2018_realistic_v9-v1_list.txt

  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': ${N_PU}}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"
  # --pileup_input /store/mc/RunIIFall18GS/MinBias_TuneCP5_13TeV-pythia8/GEN-SIM/102X_upgrade2018_realistic_v9-v1/90013/18A5353D-9492-E811-A9DC-24BE05C488E1.root
else
  cmsDriver.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1
fi

echo "--> Running step 2"
date
cmsRun step2_${output_flag}_RAW_cfg.py &> step2.log
rm ${output_flag}_GEN-SIM.root


echo "Step 3: RAW -> AOD"
date
cmsDriver.py --filein file:${output_flag}_RAW.root --fileout file:${output_flag}_AODSIM.root --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 2 --era Run2_2018 --python_filename step3_${output_flag}_AODSIM_cfg.py --no_exec -n -1

echo "--> Running step 3"
date
cmsRun step3_${output_flag}_AODSIM_cfg.py &> step3.log
rm ${output_flag}_RAW.root


echo "Step 4: AOD -> MINIAOD"
date
cmsDriver.py --filein file:${output_flag}_AODSIM.root --fileout file:${output_flag}_MINIAODSIM.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 102X_upgrade2018_realistic_v15 --step PAT --era Run2_2018 --nThreads 2 --python_filename step4_${output_flag}_MINIAODSIM_cfg.py --no_exec -n -1

echo "--> Running step 4"
date
cmsRun step4_${output_flag}_MINIAODSIM_cfg.py &> step4.log
rm ${output_flag}_AODSIM.root

echo "Generation finished"
date

if [ -z "$ntuplizer_config" ]
then
  echo "No ntuplizer"
else
  echo "Step 5: MINIAOD -> CAND"
  date
  if [ `uname -n` = "login-1.hep.caltech.edu" ]; then
    cd /storage/user/ocerri/work/CMSSW_10_2_3/src/ntuplizer/BPH_RDntuplizer
  else
    cd /afs/cern.ch/user/o/ocerri/work/CMSSW_10_2_3/src/ntuplizer/BPH_RDntuplizer
  fi
  eval `scramv1 runtime -sh`
  echo "--> Running step 5"
  date
  cmsRun config/$ntuplizer_config inputFile=$out_dir/test_MINIAODSIM.root outputFile=$out_dir/test_CAND.root &> $out_dir/step5.log
fi

echo "Job finished"
date
