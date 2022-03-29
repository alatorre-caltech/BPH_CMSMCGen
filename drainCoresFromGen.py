#!/usr/bin/env python
import os, json, argparse, commands, datetime, time
import numpy as np

jobStatusDic = {'idle':1, 'running':2, 'hold':5}

parser = argparse.ArgumentParser(description='Free cores from matching condor jobs.',
                                 epilog='Test example: ./drainCoresFromGen.py',
                                 add_help=True
                                 )
parser.add_argument ('--batch_name', default=['gen_.*'], help='Patter used to match BATCH_NAME.', nargs='+')
parser.add_argument ('--nToFree', '-n', type=int, default=10, help='Number of jobs to put on hold.')
args = parser.parse_args()

cmd = 'condor_hold -constraint \'('
cmd += ' || '.join(['regexp("'+p+'",JobBatchName)' for p in args.batch_name])
cmd += ') && JobStatus == ' + str(jobStatusDic['idle'])
cmd += '\''
print cmd
status, output = commands.getstatusoutput(cmd)
if status:
    print output
    exit()

cmd = 'condor_q -json -constraint \'('
cmd += ' || '.join(['regexp("'+p+'",JobBatchName)' for p in args.batch_name])
cmd += ') && JobStatus == ' + str(jobStatusDic['running'])
cmd += '\''
print cmd
status, output = commands.getstatusoutput(cmd)
if status:
    print output
    exit()

matching_jobs = json.loads(output)
jobs_id = []
jobs_running_time = []
n_idle2hold = 0
for job in matching_jobs:
    auxId =  str(job['ClusterId'])+'.'+str(job['ProcId'])
    if job['JobStatus'] == jobStatusDic['idle']:
        os.system('condor_hold ' + auxId + ' 2>&1 > /dev/null')
        n_idle2hold += 1
    elif job['JobStatus'] == jobStatusDic['running']:
        jobs_id.append(auxId)
        jobs_running_time.append(time.time() - job['JobCurrentStartDate'])
print 'Job on idle held', n_idle2hold
wasted_time = 0
for i in np.argsort(jobs_running_time)[:args.nToFree]:
    wasted_time += jobs_running_time[i]
    os.system('condor_hold ' + jobs_id[i])
print 'Average wall time wasted:', str(datetime.timedelta(seconds=np.ceil(wasted_time/args.nToFree)))
print 'Total CPU time wasted:', str(datetime.timedelta(seconds=np.ceil(wasted_time)))
# print jobs_id[i], str(datetime.timedelta(seconds=jobs_running_time[i]))
