import os, commands, sys

minBias_dataset='/MinBias_TuneCP5_13TeV-pythia8/RunIIFall18GS-102X_upgrade2018_realistic_v9-v1/GEN-SIM'

cmd = 'das_client --query="file dataset='+minBias_dataset+'" --limit=0'
sys.stdout.write('Fetching '+minBias_dataset+' files list from das_client...')
status, output = commands.getstatusoutput(cmd)
print 'done with status',status,'\n'

print 'Dumping LFN list'
with open('minBiasFilesList_LFN.txt', 'w') as f:
    f.write(output+'\n')

print 'Dumping local path list'
flist = output.split('\n')
nF = float(len(flist))
nFound = 0
with open('minBiasFilesList_localPath.txt', 'w') as f:
    for i, ln in enumerate(flist):
        if i > 0:
            sys.stdout.write('\r')
        sys.stdout.write('{:.0f} %'.format(100*(i+1)/float(nF)))
        sys.stdout.flush()
        if i == nF -1:
            print ' done'
            # print '{:.1f} %'.format(100*(i+1)/float(nF))
        floc = '/storage/cms' + ln.strip()
        if os.path.isfile(floc):
            nFound += 1
            f.write('file:'+floc + '\n')
print 'Files found: {} ({:.1f}%)'.format(nFound, 100*nFound/nF)
