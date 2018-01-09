#!/usr/bin/env python

import logging
import os
import sys

def cmd(command):
  logging.info('Executing: %s...', command)
  err = os.system(command)
  if err == 0:
    logging.info('Executing: %s: done', command)
  else:
    logging.warn('Executing: %s: failed with return code %i', command, err)
  
  return err == 0

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
for line in open('cfg/sample-metadata.csv', 'r'):
  if line.startswith('#'):
    continue


  # the brass file is ./WGS_775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52/brass/775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52.annot.vcf.gz
  # caveman annot.muts.vcf.gz
  f = line.strip('\n').split(',')
  if f[4] == 'N':
    sample=f[0]
    #if cmd('tar xvfz ./out/{sample}.wgs.1.1.2/WGS_*.result.tar.gz "*.annot.vcf.gz*"'.format(sample=sample)):
    #  cmd('mv ./WGS_*/brass/*.vcf.gz ./out/{sample}.brass-1.1.2.vcf.gz'.format(sample=sample))
    #  cmd('mv ./WGS_*/brass/*.vcf.gz.tbi ./out/{sample}.brass-1.1.2.vcf.gz.tbi'.format(sample=sample))
    #  cmd('rm -r WGS_*')

    
    #if cmd('tar xvfz ./out/{sample}.wgs.1.1.2/WGS_*.result.tar.gz "*.muts.ids.vcf.gz*"'.format(sample=sample)):
    #  cmd('mv ./WGS_*/caveman/*.muts.ids.vcf.gz ./out/{sample}.caveman-1.1.2.vcf.gz'.format(sample=sample))
    #  cmd('mv ./WGS_*/caveman/*.muts.ids.vcf.gz.tbi ./out/{sample}.caveman-1.1.2.vcf.gz.tbi'.format(sample=sample))
    #  cmd('rm -r WGS_*')

    #.flagged.muts.vcf
    if cmd('tar xvfz ./out/{sample}.wgs.1.1.2/WGS_*.result.tar.gz "*.flagged.muts.vcf"'.format(sample=sample)):
      cmd('mv ./WGS_*/caveman/*.flagged.muts.vcf ./out/{sample}.caveman.flagged.vcf'.format(sample=sample))
      cmd('rm -r WGS_*')

    #if cmd('tar xvfz ./out/{sample}.wgs/WGS_*.result.tar.gz "*.muts.ids.vcf.gz*"'.format(sample=sample)):
    #  cmd('mv ./WGS_*/caveman/*.muts.ids.vcf.gz ./out/{sample}.caveman.vcf.gz'.format(sample=sample))
    #  cmd('mv ./WGS_*/caveman/*.muts.ids.vcf.gz.tbi ./out/{sample}.caveman.vcf.gz.tbi'.format(sample=sample))
    #  cmd('rm -r WGS_*')

    # ascat
    # ./WGS_775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52/brass/775021c4-50ef-48e4-b9d7-bbfa959b67b4.copynumber.txt.gz
    #if 
