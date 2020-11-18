#!/usr/bin/env python
# Usage: watch -n 900 "./condorSentinel.py &>> ~/.condorSentinel/activity.log"
import os, sys, subprocess, re, json
import argparse
import commands
import time
import numpy as np
import datetime
import pickle
from glob import glob

def BladeN(job):
    s = job['RemoteHost'][:-6]
    idx = s.find('blade-')
    if idx >= 0:
        return int(s[idx+6:])
    else:
        return 99

logdir = os.environ['HOME'] + '/.condorSentinel'
if not os.path.isdir(logdir):
    os.system('mkdir ' + logdir)


print '\n' + 60*'#'
value = datetime.datetime.fromtimestamp(time.time())
print value.strftime('%Y-%m-%d %H:%M:%S')
os.system('echo ' +str(time.time()) + ' > ' + logdir + '/lastRun.log')

totCpu = 0
freeCpu = 0
for n in glob('/storage/control/userqueue/*'):
    name = os.path.basename(n)
    cmd = 'condor_status '+name+' -const \'SlotID=?=1 && SlotType=?="Partitionable"\' -af Machine Cpus DetectedCpus DetectedMemory Memory'
    status, output = commands.getstatusoutput(cmd)
    output = output.split(' ')
    totCpu += int(output[2])
    freeCpu += int(output[1])
print 'Total CPU:', totCpu
print 'Free CPU:', freeCpu

N_min_idle_to_trigger_holding = 1
N_max_my_jobs_kept_running = 0
N_max_running_jobs_to_release = 200
Min_slots_to_be_freed = 2
wait_time_to_release = 14 # minutes

status, output = commands.getstatusoutput('condor_q -all')

aux = None
nNiceOthers = {'idle':0, 'running':0}
for l in output.split('\n'):
    if l.startswith('nice-user') and not l.startswith('nice-user.ocerri'):
        data = [x for x in l.split(' ') if x]
        print data
        nNiceOthers['running'] += int(data[6])
        nNiceOthers['idle'] += int(data[7])
    if l.startswith('Total for all users:'):
        aux = l.split(';')[1][1:]
        aux = aux.split(', ')
        break
if aux is None:
    print 'Error in interpreting the condor_q output'
    print output
    print 60*'-'
    exit()

N = {}
for e in aux:
    n, status = e.split(' ')
    N[status] = int(n) - nNiceOthers.get(status, 0)
print 'All jobs (w/0 nice from other users):', N

N_nice = {}
N_nice['idle'] = 0
N_nice['running'] = 0
N_nice['hold'] = 0
status, output = commands.getstatusoutput('condor_q -json')
if output:
    jobs_list = json.loads(output)
    for job in jobs_list:
        if job['Owner'] == 'ocerri' and job['User'].startswith('nice'):
            if job['JobStatus'] == 1:
                N_nice['idle'] += 1
            elif job['JobStatus'] == 2:
                N_nice['running'] += 1
            elif job['JobStatus'] == 5:
                N_nice['hold'] += 1
print 'Nice jobs:', N_nice
print 'Non-nice jobs idle:', N['idle'] - N_nice['idle']

status, output = commands.getstatusoutput('condor_status -total')
l = output.split('\n')[-1].split(' ')
l = [x for x in l if x]
free_cpus = int(l[4])
# print 'CPUs free:', free_cpus
if N['idle'] - N_nice['idle'] < N_min_idle_to_trigger_holding:
    if N['running'] - N_nice['running'] < N_max_running_jobs_to_release and N_nice['hold'] > 0:
        if os.path.isfile(logdir + '/firstReleaseAttempt.pickle'):
            firstAttempt_time = pickle.load(open(logdir + '/firstReleaseAttempt.pickle' ,'rb'))
            if time.time() - firstAttempt_time >= wait_time_to_release * 60:
                print 'Releasing ocerri jobs'
                os.system('condor_release ocerri')
                os.system('rm ' + logdir + '/firstReleaseAttempt.pickle')
        else:
            now = time.time()
            pickle.dump(now, open(logdir + '/firstReleaseAttempt.pickle' ,'wb'))
            print 'First attempt to release jobs'
    elif N['running'] - N_nice['running'] < N_max_running_jobs_to_release and N_nice['hold'] == 0:
        os.system('rm -rf ' + logdir + '/firstReleaseAttempt.pickle')
        print 'No nice jobs on hold to release'
    elif N['running'] - N_nice['running'] > N_max_running_jobs_to_release:
        os.system('rm -rf ' + logdir + '/firstReleaseAttempt.pickle')
        print 'Queue busy'

    print 60*'-'
    exit()

if N_nice['idle'] == 0 and N_nice['running'] <= N_max_my_jobs_kept_running:
    print 'Queue busy, nothing to be done on nice jobs'
    print 60*'-'
    exit()

print 'Putting nice jobs on hold'
status, output = commands.getstatusoutput('condor_q -json')
jobs_list = json.loads(output)

running_jobs = []
N_held = 0
for job in jobs_list:
    if job['Owner'] == 'ocerri' and job['User'].startswith('nice-user.ocerri'):
        if job['JobStatus'] == 2:
            if BladeN(job) <= 8:
                running_jobs.append(job)
        if job['JobStatus'] == 1:
            continue
            # cmd = 'condor_hold '
            # cmd += job['GlobalJobId'].split('#')[1]
            # cmd += ' > /dev/null'
            # os.system(cmd)
            # N_held += 1
print N_held, 'idle -> hold'
if len(running_jobs) <=  N_max_my_jobs_kept_running:
    print 60*'-'
    exit()

# start_times = np.array([int(j['JobStartDate']) for j in running_jobs])
# sorted_idxs = np.argsort(-start_times)
# blade_number = np.array([BladeN(running_jobs[j]) for j in sorted_idxs])
# sorted_idx_blade = np.argsort(blade_number)
# sorted_idxs = sorted_idxs[sorted_idx_blade]

blade_number = np.array([BladeN(j) for j in running_jobs])
sorted_idxs = np.argsort(blade_number)

# with open('/storage/user/ocerri/orderTest.txt', 'w') as ftest:
#     for i in sorted_idxs:
#         job = running_jobs[i]
#         s = job['GlobalJobId'].split('#')[1] + '\t' + str(BladeN(job)) + '\t'
#         s += str(int(job['JobStartDate']))
#         ftest.write(s + '\n')
# exit()

N_held = 0
N_waist = 0
slot_to_be_freed = max(Min_slots_to_be_freed, N['idle'] - N_nice['idle'])
slot_to_be_freed = min(slot_to_be_freed, len(running_jobs) - N_max_my_jobs_kept_running)
idx_list = sorted_idxs[:slot_to_be_freed]

print 'Killing', len(idx_list), 'jobs'
for idx in idx_list:
    job = running_jobs[idx]
    cmd = 'condor_hold '
    cmd += job['GlobalJobId'].split('#')[1]
    cmd += ' > /dev/null'
    os.system(cmd)
    N_held += 1
    N_waist += int(time.time()) - int(job['JobStartDate'])
print N_held, 'run -> hold'
print 'CPU time waist: {:.2f} hours'.format(N_waist/3600.)
print 60*'-'
