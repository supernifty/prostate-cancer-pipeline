#!/usr/bin/env python
'''
  find status of all samples for htsdb
'''

import collections
import glob
import os
import re
import sys

counts = collections.defaultdict(int)

sys.stdout.write('#Sample,Status,Date\n')
for prefix in ('CMHS', 'APCRC'):
  for f in glob.glob('{}[0-9]*'.format(prefix)): # pre-aligned bam is at least in progress
    # prealigned CMHSnnn.bam, CMHSnnn.validation
    m = re.search('^({}[0-9NT]+).bam$'.format(prefix), f)
    if m is not None:
      modified = os.stat(f).st_mtime
      sys.stdout.write('{},prealigned,{}\n'.format(m.group(1), modified))
      counts['prealigned'] += 1
      continue
  
    # aligned CMHSnnn.mapped.bam
    m = re.search('^({}[0-9NT]+).mapped.bam$'.format(prefix), f)
    if m is not None:
      modified = os.stat(f).st_mtime
      sys.stdout.write('{},aligned,{}\n'.format(m.group(1), modified))
      counts['aligned'] += 1
      continue
  
    # aligned with qc - updated with populate_measurement
  
  # variant calling - CMHSnnn.wgs/completed.finished
  # old
  for f in glob.glob('{}[0-9]*.wgs/completed.finish'.format(prefix)): 
    sample = f.split('.')[0]
    modified = os.stat(f).st_mtime
    sys.stdout.write('{},variants,{}\n'.format(sample, modified))
    counts['variants'] += 1
  
  # ./out/CMHS360.wgs.1.1.2/completed.finish
  for f in glob.glob('{}[0-9]*.wgs.1.1.2/completed.finish'.format(prefix)): 
    sample = f.split('.')[0]
    modified = os.stat(f).st_mtime
    sys.stdout.write('{},variants,{},1.1.2\n'.format(sample, modified))
    counts['variants-1.1.2'] += 1

  for analysis in ('delly', 'gridss', 'muse', 'mutect1', 'hmmcopy', 'contest', 'sniper', 'delly2'):
    for f in glob.glob('{}[0-9]*.{}.completed'.format(prefix, analysis)):
      sample = f.split('.')[0]
      modified = os.stat(f).st_mtime
      sys.stdout.write('{},{},{}\n'.format(sample, analysis, modified))
      counts[analysis] += 1
   
sys.stderr.write('{}'.format(counts))
