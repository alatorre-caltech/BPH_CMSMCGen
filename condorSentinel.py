#!/usr/bin/env python
# Usage: watch -n 900 "./condorSentinel.py &>> ~/.condorSentinel/activity.log"
import os, sys, subprocess, re, json
import argparse
import commands
import time
import numpy as np
import datetime
import pickle

logdir = os.environ['HOME'] + '/.condorSentinel'
if not os.path.isdir(logdir):
    os.system('mkdir ' + logdir)


print '\n' + 60*'#'
value = datetime.datetime.fromtimestamp(time.time())
print value.strftime('%Y-%m-%d %H:%M:%S')
os.system('echo ' +str(time.time()) + ' > ' + logdir + '/lastRun.log')

N_min_idle_to_trigger_holding = 1
N_max_my_jobs_kept_running = 0
N_max_running_jobs_to_release = 100

status, output = commands.getstatusoutput('condor_q -all')

aux = None
for l in output.split('\n'):
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
    N[status] = int(n)
print 'All jobs:', N

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
print 'CPUs free:', free_cpus
if N['idle'] - N_nice['idle'] < N_min_idle_to_trigger_holding:
    if N['running'] - N_nice['running'] < N_max_running_jobs_to_release and N_nice['hold'] > 0:
        if os.path.isfile(logdir + '/firstReleaseAttempt.pickle'):
            firstAttempt_time = pickle.load(open(logdir + '/firstReleaseAttempt.pickle' ,'rb'))
            if time.time() - firstAttempt_time >= 30 * 60:
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
    print 'No nice jobs idle and nice running jobs below threshold'
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
            running_jobs.append(job)
        if job['JobStatus'] == 1:
            cmd = 'condor_hold '
            cmd += job['GlobalJobId'].split('#')[1]
            cmd += ' > /dev/null'
            os.system(cmd)
            N_held += 1
print N_held, 'idle -> hold'
if len(running_jobs) <=  N_max_my_jobs_kept_running:
    print 60*'-'
    exit()

start_times = np.array([j['JobStartDate'] for j in running_jobs])
sorted_idxs = np.argsort(start_times)

N_held = 0
N_waist = 0
slot_to_be_freed = max(8, N['idle'] - N_nice['idle'])
if slot_to_be_freed > 192:
    if N_max_my_jobs_kept_running > 0:
        idx_list = sorted_idxs[:-N_max_my_jobs_kept_running]
    else:
        idx_list = sorted_idxs
else:
    idx_list = sorted_idxs[:slot_to_be_freed]
print 'Killing', len(idx_list), 'jobs'
for idx in idx_list:
    job = running_jobs[idx]
    cmd = 'condor_hold '
    cmd += job['GlobalJobId'].split('#')[1]
    cmd += ' > /dev/null'
    os.system(cmd)
    N_held += 1
    N_waist += time.time() - float(job['JobStartDate'])
print N_held, 'run -> hold'
print 'CPU time waist: {:.2f} hours'.format(N_waist/3600.)
print 60*'-'
