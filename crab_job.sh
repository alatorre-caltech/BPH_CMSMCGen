#!/bin/bash
set -e
set -v

#get the
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTopic#Running_a_user_script_with_CRAB
#To be precise, CRAB job wrapper will execute scriptExe jobId <scriptArgs> where scripExe is the name passed in CRAB configuration, jobId is the number of this job in the task, and <scriptArgs> indicate optional additional arguments which can be specified in CRAB configuration file via the JobType.scriptArgs parameter
job_id=$1
N_evts=$2
st_seed=$3
process_name=$4
N_PU=$5

initial_dir=`pwd`

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh

#set up CMSSW
scramv1 project CMSSW CMSSW_10_2_3
cd CMSSW_10_2_3/src
eval `scramv1 runtime -sh`

mkdir -p Configuration/GenProduction/python
cp $initial_dir/*cfi.py Configuration/GenProduction/python/
scram b

#go back to starting directory
cd $initial_dir
mkdir out_$((st_seed+job_id))

#Run now the real job
chmod +x job1023_gen_v1.sh
./job1023_gen_v1 $N_evts $st_seed $job_id $process_name out_$((st_seed+job_id)) CMSSW_10_2_3/src $N_PU

#here need to create the FrameworkJobReport.xml which gets propagated to crab
cmsRun -j FrameworkJobReport.xml step4_${process_name}_MINIAODSIM_cfg.py
