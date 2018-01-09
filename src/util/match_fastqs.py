#!/usr/bin/env python
'''
  checks read ids and writes out new versions of gzipped fastq files
  usage:
    python match_fastqs.py inR1 inR2 outR1 outR2
'''

import gzip
import logging
import sys

def main(r1fn, r2fn, w1fn, w2fn):
  l1 = 0
  l2 = 0
  last1 = 0
  last2 = 0
  w1 = 0
  w2 = 0
  r1 = []
  r2 = []
  headers = [None, None]
  has_next = [True, True]
  #with gzip.open(r1fn, 'r') as r1fh, gzip.open(r2fn, 'r') as r2fh, gzip.open(w1fn, 'w') as w1fh, gzip.open(w2fn, 'w') as w2fh:
  with gzip.open(r1fn, 'r') as r1fh, gzip.open(r2fn, 'r') as r2fh, open(w1fn, 'w') as w1fh, open(w2fn, 'w') as w2fh:
    try:
      r1.append(r1fh.readline())
      l1 += 1
      r2.append(r2fh.readline())
      l2 += 1
      while all(has_next):
        has_next = [False, False]
        # check ids match
        if r1[-1].split(' ')[0] != r2[-1].split(' ')[0]:
          logging.error('Line {}/{}. Read IDs do not match: {} vs {}'.format(l1, l2, r1[0], r2[0]))
          # keep skipping r2 until a match is found
          r2 = r2[-1:]
          skipped = len(r2) - 1
          for line in r2fh:
            r2.append(line)
            l2 += 1
            skipped += 1
            if line.startswith('@'):
              has_next[1] = True
              if r1[-1].split(' ')[0] == r2[-1].split(' ')[0]:
                logging.error('skipped {} total'.format(skipped))
                break
              else:
                r2 = r2[-1:]
            if skipped % 100000 == 0:
              logging.error('skipped {}'.format(skipped))

        # read r1
        for line in r1fh:
          r1.append(line)
          l1 += 1
          if line.startswith('@'):
            has_next[0] = True
            break

        # read r2
        for line in r2fh:
          r2.append(line)
          l2 += 1
          if line.startswith('@'):
            has_next[1] = True
            break

        # write out both records if there's another
        if all(has_next):
          w1fh.write(''.join(r1[:-1]))
          w2fh.write(''.join(r2[:-1]))
          w1 += len(r1) - 1
          w2 += len(r2) - 1
          # remove written records
          r1 = r1[-1:]
          r2 = r2[-1:]
        else: # one or both inputs are finished
          logging.info('Final R1 record has {} lines. R2 has {} lines. Not written.'.format(len(r1), len(r2)))
 
        if l1 - last1 > 1000000:
          logging.info('{} lines read from {}'.format(l1, r1fn))
          logging.info('{} lines written to {}'.format(w1, w1fn))
          last1 = l1
        if l2 - last2 > 1000000:
          logging.info('{} lines read from {}'.format(l2, r2fn))
          logging.info('{} lines written to {}'.format(w2, w2fn))
          last2 = l2
    except:
      logging.exception('An exception occurred')

  logging.info('{} lines read from {}'.format(l1, r1fn))
  logging.info('{} lines read from {}'.format(l2, r2fn))
  logging.info('{} lines written to {}'.format(w1, w1fn))
  logging.info('{} lines written to {}'.format(w2, w2fn))

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
