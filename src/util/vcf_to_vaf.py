#!/usr/bin/env python
'''
  calculate vaf of vcf
'''

import argparse
import collections
import logging
import sys


def main():
    for line in sys.stdin:
        if line.startswith('#'):
            continue

        # 1       13116   .       T       G       .       PASS    ADP=89;WT=0;HET=0;HOM=1;NC=0    GT:GQ:SDP:DP:RD:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR    1/1:255:89:89:16:73:82.02%:1.3684E-34:34:37:8:8:20:53
        fields = line.strip().split('\t')
        info = fields[9].split(':')
        #vaf = 1. * int(info[5]) / int(info[3])
        vaf = float(info[6][:-1]) / 100.
        key = '{}/{}'.format(fields[0], fields[1])
        sys.stdout.write('{}\t{}\t{}\t{}\n'.format(key, fields[0], fields[1], vaf))
 
if __name__ == '__main__':
    main()
