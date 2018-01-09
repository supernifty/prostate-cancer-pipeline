#!/usr/bin/env python
'''
  measure concordance of homozygous snps between groups of samples
'''

import argparse
import collections
import logging
import sys

HET=0.4
HOM=0.9

def process(normals, tumors):
  normal_vafs = {}
  # 1       13116   .       T       G       .       PASS    ADP=89;WT=0;HET=0;HOM=1;NC=0    GT:GQ:SDP:DP:RD:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR    1/1:255:89:89:16:73:82.02%:1.3684E-34:34:37:8:8:20:53
  for normal in normals:
    normal_vafs[normal] = {}
    logging.info('processing %s...', normal)
    for line in open(normal, 'r'):
      if line.startswith('#'):
          continue
      fields = line.strip().split('\t')
      info = fields[9].split(':')
      #vaf = 1. * int(info[5]) / int(info[3])
      vaf = float(info[6][:-1])
      key = '{}/{}'.format(fields[0], fields[1])
      normal_vafs[normal][key] = vaf
    logging.info('processing %s: done', normal)

  concordant = collections.defaultdict(int)
  discordant = collections.defaultdict(int)
  for tumor in tumors:
    logging.info('processing %s...', tumor)
    tumor_vaf = {}
    for line in open(tumor, 'r'):
      if line.startswith('#'):
        continue
      fields = line.strip().split('\t')
      info = fields[9].split(':')
      #vaf = 1. * int(info[5]) / int(info[3])
      vaf = float(info[6][:-1])
      key = '{}/{}'.format(fields[0], fields[1])
      for normal in normals:
        if key in normal_vafs[normal]:
          normal_vaf = normal_vafs[normal][key]
          if normal_vaf >= HOM: # normal has it
            if vaf >= HOM: # tumor should have it
              concordant[normal] += 1
            else: # tumor doesn't have it
              discordant[normal] += 1
        else: # no normal, but tumor
          if vaf >= HET:
            discordant[normal] += 1

    for normal in normals:
      for key in normal_vafs[normal]:
        # hom in normal not present in tumor
        if key not in tumor_vaf and normal_vafs[normal][key] >= HOM:
          discordant[normal] += 1

      sys.stdout.write('{},{},{:.2f},{},{}\n'.format(tumor, normal, 1. * concordant[normal] / (concordant[normal] + discordant[normal]), concordant[normal], discordant[normal]))
       
    # now look for extra normals
    logging.info('processing %s: done', tumor)

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='concordance matrix')
    parser.add_argument('--normals', required=True, nargs='+', help='normal vcfs')
    parser.add_argument('--tumors', required=True, nargs='+', help='tumor vcfs')
    args = parser.parse_args()
    process(args.normals, args.tumors)

if __name__ == '__main__':
    main()
