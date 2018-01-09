#!/usr/bin/env python

import os
import sys

def cmd(c):
  sys.stderr.write('starting {}...\n'.format(c))
  os.system(c)
  sys.stderr.write('finished {}\n'.format(c))
  
def main():
  for line in open('/scratch/VR0320/pgeorgeson/pan-prostate/cfg/sample-metadata.csv', 'r'):
    # Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
    # mini,minipatient,minilab,minitissue,N,testing1,testing2,testing3
    f = line.strip('\n').split(',')
    if line.startswith('#'):
      continue
    is_normal = f[4]
    samplename = f[0]
    if is_normal == 'Y':
      cmd('mkdir -p /scratch/VR0320/pgeorgeson/pan-prostate/out/{samplename}.gatk'.format(samplename=samplename))
      cmd('sed "s/SAMPLENAME/{samplename}/" < /scratch/VR0320/pgeorgeson/pan-prostate/src/util/gatk.sh.template > /scratch/VR0320/pgeorgeson/pan-prostate/out/{samplename}.gatk/gatk.sh'.format(samplename=samplename))
      cmd('cd /scratch/VR0320/pgeorgeson/pan-prostate/out/{samplename}.gatk && sbatch /scratch/VR0320/pgeorgeson/pan-prostate/out/{samplename}.gatk/gatk.sh'.format(samplename=samplename))

if __name__ == '__main__':
  main()
