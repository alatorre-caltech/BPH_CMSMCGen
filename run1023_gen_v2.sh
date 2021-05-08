#!/bin/bash
set -e

# ------------------------------ SIGNAL ----------------------------------------
# process_name=BParking_Tag_Bd_MuNuDst_SoftQCDnonD_scale5_TuneCP5_ISGW2
# process_name=BParking_Tag_Bd_MuNuDst_SoftQCDnonD_scale1_TuneCP5_ISGW2
# process_name=BParking_Tag_Bd_MuNuDst_HardQCDhardbbbar_TuneCP5_ISGW2

# process_name=BParking_Tag_Bd_TauNuDst_SoftQCDnonD_scale5_TuneCP5_ISGW2


# ------------------------------ BACKGROUND ------------------------------------

## B(s) -> D** mu nu
# process_name=BParking_Tag_Bu_MuNuDstst_Pip_SoftQCDnonD_scale5_TuneCP5_ISGW2
# process_name=BParking_Tag_Bd_MuNuDstst_Pi0_SoftQCDnonD_scale5_TuneCP5_ISGW2
# process_name=BParking_Tag_Bd_MuNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2
# process_name=BParking_Tag_Bu_MuNuDstst_PiPi_SoftQCDnonD_scale5_TuneCP5_ISGW2

# process_name=BParking_Tag_Bu_TauNuDstst_Pip_SoftQCDnonD_scale5_TuneCP5_ISGW2
process_name=BParking_Tag_Bd_TauNuDstst_Pi0_SoftQCDnonD_scale5_TuneCP5_ISGW2

# process_name=BParking_Tag_Bs_MuNuDsstst_SoftQCDnonD_scale5_TuneCP5_ISGW2
# process_name=BParking_Tag_Bs_TauNuDsstst_SoftQCDnonD_scale5_TuneCP5_ISGW2



# ------------------------------ ANCILLARY -------------------------------------
# process_name=BParking_Bd_JpsiKst_SoftQCDnonD_scale5_TuneCP5_HELAMP





#################################################################################
##########    OLD ############################
#################################################################################

# ------------------------------ Unbiased -----------------------------------------
# process_name=Unbiased_B0_MuNuDmst_Hardbbbar_evtgen_ISGW2
# process_name=Unbiased_B0_TauNuDmst_Hardbbbar_evtgen_ISGW2
# --------------------------------------------------------------------------------

# ------------------------------ SIGNAL -----------------------------------------
# process_name=BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_HQET2_central
# process_name=BPH_Tag-B0_MuNuDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2
# process_name=BP_Tag_B0_MuNuDmst_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_antiB0_MuNuDmst_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_MuNuDmst_SoftQCDall_evtgen_ISGW2

# process_name=BPH_Tag-B0_TauNuDmst-pD0bar-kp-t2mnn_pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2
# process_name=BP_Tag_B0_TauNuDmst_Hardbbbar_evtgen_ISGW2

# process_name=BP_Probe_B0_MuNuDmst_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2
# process_name=BP_Probe_B0_TauNuDmst_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2

# ntuplizer_config=cmssw_privateMC_Tag_B0_MuDmst-pD0bar-kp.py
# --------------------------------------------------------------------------------

# ------------------------------ BACKGROUND -----------------------------------------
# process_name=BPH_Tag-Bp_MuNuDstst_DmstPi_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_ISGW2
# process_name=BPH_Tag-B0_DmstHc-pD0bar-kp-Hc2mu_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen
# process_name=BP_Tag_Bp_MuNuDstst_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_Bp_TauNuDstst_Pip_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_DmstPi0MuNu_Hardbbbar_evtgen_GR
# process_name=BP_Tag_Bp_MuNuDstst_PipPi0_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_MuNuDstst_PipPim_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_MuNuDstst_Pi0_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_TauNuDstst_Pi0_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_MuNuDstst_Pi0Pi0_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_MuNuDstPipPim_Hardbbbar_evtgen_PHSP
# process_name=BP_Tag_Bp_MuNuDstPipPi0_Hardbbbar_evtgen_PHSP
# process_name=BP_Tag_B0_MuNuDstPiPiPi_Hardbbbar_evtgen_PHSP
# process_name=BP_Tag_Bp_MuNuDstPiPiPi_Hardbbbar_evtgen_PHSP
# process_name=BP_Tag_B0_DmstHc_Hardbbbar_evtgen_ISGW2 #Deprecated
# process_name=BP_Tag_B0_DstmDsp_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_DstmD0_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_B0_DstmDp_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_Bm_DstmHc_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_Bp_DstmHc_Hardbbbar_evtgen_ISGW2
# process_name=BP_Tag_antiB0_DstmHc_Hardbbbar_evtgen_ISGW2

# process_name=BP_Tag_B0_KpDmst_Hardbbbar_evtgen_SVS

# process_name=BP_Probe_Bp_MuNuDstst_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2
# process_name=BP_Probe_B0_DmstHc_Tag-B_MuNuDst_Hardbbbar_evtgen_ISGW2

# ntuplizer_config=cmssw_privateMC_Tag_B0_MuDmst-pD0bar-kp.py
# --------------------------------------------------------------------------------

# ------------------------------ CONTROL REGION ----------------------------------
# process_name=BPH_Tag-Mu_Probe-B0_KDmst-pD0bar-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVS
# process_name=BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgen_SVV
# process_name=BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_Hardbbbar_PTFilter5_0p0-evtgenFSR_SVV
# process_name=BPH_Tag-Probe_B0_JpsiKst-mumuKpi-kp_13TeV-pythia8_SoftQCD_PTFilter5_0p0-evtgen_SVV
# process_name=BP_Tag-Probe_B0_JpsiKst_Hardbbbar_evtgen_HELAMP
# process_name=BP_Tag-Probe_B0_JpsiKst_SoftQCD_evtgen_HELAMP
# process_name=BP_Tag-Probe_Bp_JpsiK_Hardbbbar_evtgen_HELAMP

# ntuplizer_config=cmssw_privateMC_Tag_Mu-Probe-B0_KDmst-pD0bar-kp.py
# ntuplizer_config=cmssw_privateMC_Tag_Mu-Probe-B0_JpsiKst-mumuKpi.py
# --------------------------------------------------------------------------------

# ------------------------------ Tracks Tag and probe ----------------------------------
# process_name=BP_Probe_B0_DmstPi_Tag-B_MuNuDst_Hardbbbar_evtgen

# ntuplizer_config=cmssw_privateMC_TagAndProbe_B0_Dmstpi.py
# --------------------------------------------------------------------------------

# ---------------------------- Test ---------------------------------------------
# process_name=PPD-RunIIFall18wmLHEGS-00010

output_flag=test

# N_PU=c0
N_PU=GENOnly

version=PU${N_PU}_10-2-3
out_loc=/afs/cern.ch/user/o/ocerri/cernbox/BPhysics/data/cmsMC_private
if [ `uname -n` = "login-1.hep.caltech.edu" ]; then
  out_loc=/storage/user/ocerri/BPhysics/data/cmsMC_private
fi
N_evts=$1
# N_evts=5000

out_dir=$out_loc/${process_name}_$version
MC_frag_file=$PWD/Configuration/GenProduction/python/${process_name}_cfi.py
EvtGen_dec_file=$PWD/GeneratorInterface/EvtGenInterface/data/evt_voc1.pdl

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

mkdir -p Configuration/GenProduction/python
cp $MC_frag_file Configuration/GenProduction/python/${process_name}_cfi.py

mkdir -p customDecayFiles
cp $EvtGen_dec_file customDecayFiles/

scram b -j12

echo "Starting job after compilation"
echo
echo "Step 1: GEN-SIM"
date

evtContent="RAWSIM"
steps="GEN,SIM"
if [ "$N_PU" == "GENonly" ]
then
  evtContent="GENRAW"
  steps="GEN"
fi

cmsDriver.py Configuration/GenProduction/python/${process_name}_cfi.py --fileout file:${output_flag}_GEN-SIM.root --mc --eventcontent $evtContent --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v15 --beamspot Realistic25ns13TeVEarly2018Collision --step $steps --nThreads 1 --geometry DB:Extended --era Run2_2018 --python_filename step1_${output_flag}_GEN-SIM_cfg.py --no_exec -n $N_evts --customise Configuration/DataProcessing/Utils.addMonitoring

echo "process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(1)" >> step1_${output_flag}_GEN-SIM_cfg.py
echo "process.MessageLogger.cerr.FwkReport.reportEvery = 100" >> step1_${output_flag}_GEN-SIM_cfg.py
echo "process.source.firstRun = cms.untracked.uint32(6741)" >> step1_${output_flag}_GEN-SIM_cfg.py


mv ./step1_${output_flag}_GEN-SIM_cfg.py $out_dir/
mkdir -p $out_dir/Configuration/GenProduction/python
cp Configuration/GenProduction/python/${process_name}_cfi.py $out_dir/Configuration/GenProduction/python/${process_name}_cfi.py

cd $out_dir

echo "--> Running step 1"
date
cmsRun -e -j step1_rt.xml step1_${output_flag}_GEN-SIM_cfg.py &> step1.log
exitcode=$?

if [ "$N_PU" == "GENonly" ]
then
  echo "Job finished"
  date
  exit $exitcode
fi

echo "Step 2: GEN-SIM -> RAW"
date

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
elif [ "$N_PU" == "c2" ]
then
  echo "Custom pileup: $N_PU"
  cmsDriver.py --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --step DIGI,L1,DIGI2RAW,HLT:@relval2018 --nThreads 2 --era Run2_2018 --filein file:${output_flag}_GEN-SIM.root --fileout file:${output_flag}_RAW.root --python_filename step2_${output_flag}_RAW_cfg.py --no_exec -n -1 --geometry DB:Extended --pileup "AVE_25_BX_25ns,{'N': 30}" --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM"

  sed -i "87iprocess.mix.input.nbPileupEvents = cms.PSet(probFunctionVariable=cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99), probValue=cms.vdouble(1.286e-05,4.360e-05,1.258e-04,2.721e-04,4.548e-04,7.077e-04,1.074e-03,1.582e-03,2.286e-03,3.264e-03,4.607e-03,6.389e-03,8.650e-03,1.139e-02,1.456e-02,1.809e-02,2.190e-02,2.589e-02,2.987e-02,3.362e-02,3.686e-02,3.938e-02,4.100e-02,4.173e-02,4.178e-02,4.183e-02,4.189e-02,4.194e-02,4.199e-02,4.205e-02,4.210e-02,4.178e-02,4.098e-02,3.960e-02,3.761e-02,3.504e-02,3.193e-02,2.840e-02,2.458e-02,2.066e-02,1.680e-02,1.320e-02,9.997e-03,7.299e-03,5.139e-03,3.496e-03,2.305e-03,1.479e-03,9.280e-04,5.729e-04,3.498e-04,2.120e-04,1.280e-04,7.702e-05,4.618e-05,2.758e-05,1.641e-05,9.741e-06,5.783e-06,3.446e-06,2.066e-06,1.248e-06,7.594e-07,4.643e-07,2.842e-07,1.734e-07,1.051e-07,6.304e-08,3.733e-08,2.179e-08,1.251e-08,7.064e-09,3.920e-09,2.137e-09,1.144e-09,6.020e-10,3.111e-10,1.579e-10,7.880e-11,3.866e-11,1.866e-11,8.864e-12,4.148e-12,1.914e-12,8.721e-13,3.928e-13,1.753e-13,7.757e-14,3.413e-14,1.496e-14,6.545e-15,2.862e-15,1.253e-15,5.493e-16,2.412e-16,1.060e-16,4.658e-17,2.045e-17,8.949e-18,3.899e-18), histoFileName=cms.untracked.string('histoPileupProbFunction.root'))" step2_${output_flag}_RAW_cfg.py
  # echo $str >> step2_${output_flag}_RAW_cfg.py
  sed -i "86d" step2_${output_flag}_RAW_cfg.py
  sed -i "86iprocess.mix.input.type = cms.string('probFunction')" step2_${output_flag}_RAW_cfg.py
else
  echo "No recognized pileup information"
  exit
fi

echo "--> Running step 2"
date
cmsRun -e -j step2_rt.xml step2_${output_flag}_RAW_cfg.py &> step2.log
# rm ${output_flag}_GEN-SIM.root


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
  if [ `uname -n` = "login-1.hep.caltech.edu" ]
  then
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
