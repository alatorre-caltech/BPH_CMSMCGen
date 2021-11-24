import os, commands
import argparse
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument ('inputDir', type=str, default='tmp/crab_*', help='Input dir template for glob', nargs='+')
parser.add_argument ('--long', default=False, action='store_true')
parser.add_argument ('--short', default=False, action='store_true')
parser.add_argument ('--verboseErrors', default=False, action='store_true')
args = parser.parse_args()

for dir in args.inputDir:
    if os.path.isdir(dir):
        print '\n' + 20*'#' + 50*'-' + 20*'#'
        cmd = 'source /cvmfs/cms.cern.ch/crab3/crab.sh; '
        cmd += 'crab status -d ' + dir
        if args.verboseErrors:
            cmd += ' --verboseErrors'
        if args.long:
            cmd += ' --long'
        if args.short:
            stats, output = commands.getstatusoutput(cmd)
            outLines = output.split('\n')
            print outLines[0][outLines[0].find('tmp/crab_') + 9: ]
            for i, l in enumerate(outLines):
                if l.startswith('Jobs status:'):
                    print '\n'.join(outLines[i:i+7])
                    break
        else:
            os.system(cmd)

        # print 20*'#' + 50*'-' + 20*'#' + '\n\n'
if not args.short:
    print 'For info on exit codes visit: https://twiki.cern.ch/twiki/bin/viewauth/CMSPublic/JobExitCodes'
