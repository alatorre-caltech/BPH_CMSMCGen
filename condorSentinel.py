#!/usr/bin/env python
# Usage: watch -n 600 "python condorSentinel.py &>> ~/.condorSentinel/activity.log"
import os, sys, subprocess, re, json
import argparse
import commands
import time
import numpy as np
import datetime

logdir = os.environ['HOME'] + '/.condorSentinel'
if not os.path.isdir(logdir):
    os.system('mkdir ' + logdir)


print '\n' + 30*'#'
value = datetime.datetime.fromtimestamp(time.time())
print value.strftime('%Y-%m-%d %H:%M:%S')
os.system('echo ' +str(time.time()) + ' > ' + logdir + '/lastRun.log')

N_min_idle_to_trigger_holding = 20
N_max_my_jobs_kept_running = 50
N_max_running_jobs_to_reease = 30

status, output = commands.getstatusoutput('condor_q -all')

for l in output.split('\n'):
    if l.startswith('Total for all users:'):
        aux = l.split(';')[1][1:]
        aux = aux.split(', ')
        break

N = {}
for e in aux:
    n, status = e.split(' ')
    N[status] = int(n)
print N

N_nice = {}
N_nice['idle'] = 0
N_nice['running'] = 0
N_nice['hold'] = 0
status, output = commands.getstatusoutput('condor_q -json')
jobs_list = json.loads(output)
for job in jobs_list:
    if job['Owner'] == 'ocerri' and job['User'].startswith('nice'):
        if job['JobStatus'] == 1:
            N_nice['idle'] += 1
        elif job['JobStatus'] == 2:
            N_nice['running'] += 1
        elif job['JobStatus'] == 5:
            N_nice['hold'] += 1
print N_nice

if N['idle'] - N_nice['idle'] < N_min_idle_to_trigger_holding:
    if N['running'] - N_nice['running'] < N_max_running_jobs_to_reease and N_nice['hold'] > 0:
        os.system('condor_release ocerri')
        print 'Releasing ocerri jobs'
    elif N['running'] - N_nice['running'] < N_max_running_jobs_to_reease and N_nice['hold'] == 0:
        print 'No nice jobs on hold to release'
    elif N['running'] - N_nice['running'] > N_max_running_jobs_to_reease:
        print 'Queue busy'
    exit()

if N_nice['idle'] == 0 and N_nice['running'] <= N_max_my_jobs_kept_running:
    print 'No nice jobs idle and nice running jobs below threshold'
    exit()

print 'Putting nice jobs in idle'
status, output = commands.getstatusoutput('condor_q -json')
jobs_list = json.loads(output)

running_jobs = []
N_held = 0
for job in jobs_list:
    if job['Owner'] == 'ocerri' and job['User'].startswith('nice'):
        if job['JobStatus'] == 2:
            running_jobs.append(job)
        if job['JobStatus'] == 1:
            cmd = 'condor_hold '
            cmd += job['GlobalJobId'].split('#')[1]
            os.system(cmd)
            N_held += 1
print N_held, 'idle -> hold'
if len(running_jobs) <=  N_max_my_jobs_kept_running:
    exit()

start_times = np.array([j['JobStartDate'] for j in running_jobs])
sorted_idxs = np.argsort(start_times)

N_held = 0
N_waist = 0
for idx in sorted_idxs[:-N_max_my_jobs_kept_running]:
    job = running_jobs[idx]
    cmd = 'condor_hold '
    cmd += job['GlobalJobId'].split('#')[1]
    os.system(cmd)
    N_held += 1
    N_waist += time.time() - float(job['JobStartDate'])
print N_held, 'run -> hold'
print 'CPU time waist: {:.2f} hours'.format(N_waist/3600.)
