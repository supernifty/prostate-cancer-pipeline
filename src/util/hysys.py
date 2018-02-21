#!/usr/bin/env python
'''
  runs hysys

  usage:
    python hysys.py < cfg/sample-metadata.csv

Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
mini,minipatient,minilab,minitissue,N,testing1,testing2,testing3

'''

import logging
import sys
import os
import os.path

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

normals = []
tumors = []
both = []
for line in sys.stdin:
  fields = line.strip('\n').split(',')
  sample = fields[0]
  # want to create sample.varscan.filtered.vcf
  
  # input exists, either input doesn't exist or has size zero
  if os.path.isfile('./out/{sample}.varscan.vcf'.format(sample=sample)):
    # input exists
    if not os.path.isfile('./out/{sample}.hysys'.format(sample=sample)) or os.stat('./out/{sample}.hysys'.format(sample=sample)).st_size == 0:
      command = 'bedtools intersect -a ./out/{sample}.varscan.vcf -b ./reference-misc/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf -sorted | python ./src/util/vcf_to_vaf.py > ./out/{sample}.hysys'.format(sample=sample)
      logging.info('executing %s...', command)
      os.system(command)
      logging.info('executing %s: done', command)
    else:
      logging.info('skipping %s out has size %i', sample, os.stat('./out/{sample}.hysys'.format(sample=sample)).st_size)
  else:
    logging.info('skipping %s: no input available', sample)

  if os.path.isfile('./out/{sample}.hysys'.format(sample=sample)):
    is_normal = fields[4] == 'Y'
    if is_normal:
      normals.append(sample)
    else:
      tumors.append(sample)
    both.append(sample)

# write tumors and normals
with open('normals.hysys', 'w') as fh:
  #fh.write('\n'.join(['./out/{}.hysys'.format(x) for x in normals]))
  fh.write('\n'.join(['./out/{}.hysys'.format(x) for x in both]))
with open('tumors.hysys', 'w') as fh:
  #fh.write('\n'.join(['./out/{}.hysys'.format(x) for x in tumors]))
  fh.write('\n'.join(['./out/{}.hysys'.format(x) for x in both]))

# now run hysys
command = 'bash tools/HaveYouSwappedYourSamples/HaveYouSwappedYourSamples.sh conc tumors.hysys normals.hysys hysys.out'
logging.info('executing %s...', command)
os.system(command)
logging.info('executing %s: done', command)
