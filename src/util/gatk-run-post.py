#!/usr/bin/env python

import os
import sys

CHROMOSOMES="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X Y MT GL000207.1 GL000226.1 GL000229.1 GL000231.1 GL000210.1 GL000239.1 GL000235.1 GL000201.1 GL000247.1 GL000245.1 GL000197.1 GL000203.1 GL000246.1 GL000249.1 GL000196.1 GL000248.1 GL000244.1 GL000238.1 GL000202.1 GL000234.1 GL000232.1 GL000206.1 GL000240.1 GL000236.1 GL000241.1 GL000243.1 GL000242.1 GL000230.1 GL000237.1 GL000233.1 GL000204.1 GL000198.1 GL000208.1 GL000191.1 GL000227.1 GL000228.1 GL000214.1 GL000221.1 GL000209.1 GL000218.1 GL000220.1 GL000213.1 GL000211.1 GL000199.1 GL000217.1 GL000216.1 GL000215.1 GL000205.1 GL000219.1 GL000224.1 GL000223.1 GL000195.1 GL000212.1 GL000222.1 GL000200.1 GL000193.1 GL000194.1 GL000225.1 GL000192.1 NC_007605 hs37d5"

def cmd(c):
  sys.stderr.write('starting {}...\n'.format(c))
  os.system(c)
  sys.stderr.write('finished {}\n'.format(c))
  
def main():
  samplenames = []
  for line in open('/scratch/VR0320/pgeorgeson/pan-prostate/cfg/sample-metadata.csv', 'r'):
    # Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
    # mini,minipatient,minilab,minitissue,N,testing1,testing2,testing3
    if line.startswith('#'):
      continue
    f = line.strip('\n').split(',')
    is_normal = f[4]
    samplename = f[0]
    if is_normal == 'Y':
      samplenames.append(samplename)

    variants = ' '.join(['--variant $ROOT/out/{samplename}.gatk/{samplename}.g.vcf.gz'.format(samplename=samplename) for samplename in samplenames])

  cmd('mkdir -p /scratch/VR0320/pgeorgeson/pan-prostate/out/gatk/')
  for chromosome in CHROMOSOMES:
    cmd('sed "s/CHROMOSOME/{chromosome}/; s/VARIANT_LIST/{variant_list}/g" < /scratch/VR0320/pgeorgeson/pan-prostate/src/util/gatk-joint.sh > /scratch/VR0320/pgeorgeson/pan-prostate/out/gatk/gatk-joint-{chromosome}.sh'.format(chromosome=chromosome, variant_list=variants.replace('/', '\\/').replace('$', '\\$')))
    #cmd('cd /scratch/VR0320/pgeorgeson/pan-prostate/out/gatk && sbatch /scratch/VR0320/pgeorgeson/pan-prostate/out/gatk/gatk-joint-{chromosome}.sh'.format(chromosome=chromosome))
    break

if __name__ == '__main__':
  main()
