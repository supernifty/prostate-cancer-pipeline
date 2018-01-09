#!/usr/bin/env python

import collections
import sys

MIN_NR=10

def main(args):
    if args[1] == 'tumorfirst':
      tumorfirst = True
    else:
      tumorfirst = False

    #nr_col = int(args[2]) # platypus=4, mutect=3

    stats = {'somatic': 0, 'germline': 0, 'pass': 0}

    #1       10066   .       C       CT      71      badReads;MQ;QD  BRF=0.92;FR=0.4967;HP=2;HapScore=1;MGOF=126;MMLQ=27;MQ=13.16;NF=88;NR=5;PP=71;QD=0.870967741935;SC=AACCCTAACCCTAACCCTAAC;SbPval=0.27;Source=Platypus;TC=134;TCF=129;TCR=5;TR=93;WE=10093;WS=10029       GT:GL:GOF:GQ:NR:NV      0/1:-1.86,0.0,-297.41:126:19:92:70      0/1:-1.77,0.0,-148.28:73:18:42:23
    for i, line in enumerate(sys.stdin):
        if line.startswith('#'):
            sys.stdout.write(line)
            continue
        if tumorfirst:
          tumor = line.strip('\n').split('\t')[9].split(':')
          normal = line.strip('\n').split('\t')[10].split(':')
        else:
          tumor = line.strip('\n').split('\t')[10].split(':')
          normal = line.strip('\n').split('\t')[9].split(':')

        if tumor[0] == normal[0]:
            stats['germline'] += 1
        else:
            stats['somatic'] += 1
            #if 'PASS' in line or 'alleleBias' in line:
            if 'PASS' in line:
                # count NR in tumor
                # platypus
                #nr = sum([int(x) for x in tumor[nr_col].split(',')])
                #if nr == 0:
                #    sys.stderr.write('{}\n'.format(i))
                #stats['nr'][nr] += 1
                #if nr > MIN_NR:
                stats['pass'] += 1
                sys.stdout.write(line)

        if i % 100000 == 0:
            sys.stderr.write('{} lines written. {} somatic {} germline {} passed\n'.format(i, stats['somatic'], stats['germline'], stats['pass']))

    sys.stderr.write('{} somatic. {} germline. {} passed.\n'.format(stats['somatic'], stats['germline'], stats['pass']))
    #sys.stderr.write('{}\n'.format(', '.join(['{}: {}'.format(k, stats['nr'][k]) for k in sorted(stats['nr'])])))

if __name__ == '__main__':
    main(sys.argv)
