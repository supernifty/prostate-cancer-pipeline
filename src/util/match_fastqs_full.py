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
  r1_ids = {}
  found = 0
  not_found = 0

  try:
    with gzip.open(r1fn, 'r') as r1fh:
      for line in r1fh:
        if line.startswith('@'):
          r1_id = line.split(' ')[0]
          r1_ids[r1_id] = -1
          if len(r1_ids) % 1000000 == 0:
            logging.info('%i R1 ids added', len(r1_ids))
    logging.info('%i R1 ids total', len(r1_ids))
  
    with gzip.open(r2fn, 'r') as r2fh:
      for idx, line in enumerate(r2fh):
        if line.startswith('@'):
          r2_id = line.split(' ')[0]
          if r2_id in r1_ids:
            r1_ids[r2_id] = idx # keep all the line numbers
            found += 1
          else:
            logging.warn('%s not found in R2', r2_id)
            not_found += 1
  
          if found % 1000000 == 0:
            logging.info('%i common ids found', found)
  except:
    logging.exception('An exception occurred')

  logging.info('%i ids total. %i found in both. %i not found in R2', len(r1_ids), found, not_found)

  # now write common reads
  try:
    written = 0
    with gzip.open(r1fn, 'r') as r1fh, gzip.open(r2fn, 'r') as r2fh, open(w1fn, 'w') as w1fh, open(w2fn, 'w') as w2fh:
      r1 = 0
      r2 = 0
      r1_id_line = r1fh.readline()
      r2_id_line = r2fh.readline()
      last_log = 0
      has_more = True
  
      while has_more:
        can_write = False
        r1_id = r1_id_line.split(' ')[0]
        if r1_id in r1_ids and r1_ids[r1_id] != -1:
          r2_target = r1_ids[r1_id]
          #logging.debug('r2_target is %i. r2 is %i', r2_target, r2)
  
          if r2_target < r2:
            # move r1 to next position
            logging.info('skipping %s in R1 on line %i, have already read past it. R2 is on line %i, need to be at line %i', r1_id, r1, r2, r1_ids[r1_id])
            while True:
              r1_id_line = r1fh.readline()
              r1 += 1
              if r1_id_line == '':
                has_more = False
                break
              if r1_id_line.startswith('@'):
                break
          elif r2_target == r2:
            can_write = True
          else: 
            # move r2 to correct position
            while r2 < r2_target:
              r2fh.readline()
              r2 += 1
            break
        else:
          logging.info('skipping %s in R1 on line %i, not in R2', r1_id, r1)
          while True:
            r1_id_line = r1fh.readline()
            r1 += 1
            if r1_id_line == '':
              has_more = False
              break
            if r1_id_line.startswith('@'):
              break
  
        if not can_write:
          continue
  
        # ready to write both records
        buffer_1 = []
        buffer_2 = []
        buffer_1.append(r1_id_line)
        buffer_2.append(r2_id_line)
        written += 1
        while True:
          r1_id_line = r1fh.readline()
          r1 += 1
          if r1_id_line == '':
            logging.info('R1 is exhausted')
            has_more = False
            break
          if r1_id_line.startswith('@'):
            break
          buffer_1.append(r1_id_line)
  
        while True:
          r2_id_line = r2fh.readline()
          r2 += 1
          if r2_id_line == '':
            logging.info('R2 is exhausted')
            has_more = False
            break
          if r2_id_line.startswith('@'):
            break
          buffer_2.append(r2_id_line)
          written += 1

        #logging.debug(buffer_1)
        # write both buffers
        w1fh.write(''.join(buffer_1))
        w2fh.write(''.join(buffer_2))
  
        if written - last_log > 1000000:
          logging.info('wrote %i lines', written)
          last_log = written
  except:
    logging.exception('An exception occurred')
      
  logging.info('wrote %i lines', written)

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
