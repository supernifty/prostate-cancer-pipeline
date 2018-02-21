#!/usr/bin/env python3

import gzip
import logging
import os
import random
import sys

#A="/scratch/VR0211/pan-prostate/out/CMHS113.wgs"
#B="/scratch/VR0211/pan-prostate/out/CMHS113.wgs.1.1.2"
A="/scratch/VR0211/pan-prostate/out/CMHS113.cgpwgs.docker.tgz"
B="/scratch/VR0211/pan-prostate/out/CMHS113.wgs.1.1.2"
TMP="./tmp"

def run(c):
  logging.info('running {}...'.format(c))
  os.system(c)
  logging.info('running {}: done'.format(c))

def compare(f1, f2):
  f1s = set()
  f2s = set()
  for line in gzip.open(f1, 'r'):
    if line.startswith('#'):
      continue
    f = line.strip('\n').split('\t')
    #CHROM  POS     ID      REF     ALT
    key = '{}/{}/{}/{}'.format(f[0], f[1], f[3], f[4])
    f1s.add(key)

  for line in gzip.open(f2, 'r'):
    if line.startswith('#'):
      continue
    f = line.strip('\n').split('\t')
    #CHROM  POS     ID      REF     ALT
    key = '{}/{}/{}/{}'.format(f[0], f[1], f[3], f[4])
    f2s.add(key)

  sys.stdout.write('common to both: {}\n'.format(len(f1s.intersection(f2s))))
  sys.stdout.write('only in a {}: {}\n'.format(len(f1s.difference(f2s)), f1s.difference(f2s)))
  sys.stdout.write('only in b {}: {}\n'.format(len(f2s.difference(f1s)), f2s.difference(f1s)))

def main():
  # extract all vcfs
  #r = int(random.random() * 1000)
  r = 502

  # extract
  run('mkdir -p {}/{}/a'.format(TMP, r))
  run('mkdir -p {}/{}/b'.format(TMP, r))
  run('cd {}/{}/a && tar xvfz {} "*.vcf.gz"'.format(TMP, r, A))
  #run('cd {}/{}/a && tar xvfz {}/WGS_*.result.tar.gz "*.vcf.gz"'.format(TMP, r, A))
  run('cd {}/{}/b && tar xvfz {}/WGS_*.result.tar.gz "*.vcf.gz"'.format(TMP, r, B))

  # compare each
  # ./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/brass
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/brass/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.annot.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/pindel
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/pindel/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.flagged.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/pindel/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.annot.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/caveman
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/caveman/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.annot.muts.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/caveman/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.muts.ids.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/caveman/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.flagged.muts.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/caveman/613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929.snps.ids.vcf.gz
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/ascat
  #./WGS_613bbbbd-ea5c-4d7c-8280-e8452f8ac305_vs_50346a9c-e4bb-44cb-b0c7-305eb27ca929/ascat/613bbbbd-ea5c-4d7c-8280-e8452f8ac305.copynumber.caveman.vcf.gz

  #run('printf "BRASS\n=====\n" > {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  sys.stdout.write('BRASS\n=====\n')

  run('cp {tmp}/{r}/a/*/brass/*.annot.vcf.gz {tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r))
  run('cp {tmp}/{r}/b/*/brass/*.annot.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  compare('{tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r), '{tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  
  #run('printf "PINDEL\n======\n" >> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  sys.stdout.write('PINDEL\n=====\n')
#
  run('cp {tmp}/{r}/a/*/pindel/*.annot.vcf.gz {tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r))
  run('cp {tmp}/{r}/b/*/pindel/*.annot.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  #run('vt partition {tmp}/{r}/cgpwgs108.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz 2>> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  compare('{tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r), '{tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  
  #run('printf "CAVEMAN\n======\n" >> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  sys.stdout.write('CAVEMAN\n=====\n')

  run('cp {tmp}/{r}/a/*/caveman/*.muts.ids.vcf.gz {tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r))
  run('cp {tmp}/{r}/b/*/caveman/*.muts.ids.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  #run('vt partition {tmp}/{r}/cgpwgs108.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz 2>> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  compare('{tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r), '{tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))

  #run('printf "CAVEMAN GERMLINE\n======\n" >> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  sys.stdout.write('CAVEMAN GERMLINE\n=====\n')

  run('cp {tmp}/{r}/a/*/caveman/*.snps.ids.vcf.gz {tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r))
  run('cp {tmp}/{r}/b/*/caveman/*.snps.ids.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  #run('vt partition {tmp}/{r}/cgpwgs108.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz 2>> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  compare('{tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r), '{tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  
  #run('printf "ASCAT\n======\n" >> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  sys.stdout.write('ASCAT\n=====\n')

  run('cp {tmp}/{r}/a/*/ascat/*.copynumber.caveman.vcf.gz {tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r))
  run('cp {tmp}/{r}/b/*/ascat/*.copynumber.caveman.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  #run('vt partition {tmp}/{r}/cgpwgs108.vcf.gz {tmp}/{r}/cgpwgs112.vcf.gz 2>> {tmp}/{r}/result.out'.format(tmp=TMP, r=r))
  compare('{tmp}/{r}/cgpwgs108.vcf.gz'.format(tmp=TMP, r=r), '{tmp}/{r}/cgpwgs112.vcf.gz'.format(tmp=TMP, r=r))
  
  
  

  #run('rm -r "{}/{}"'.format(TMP, r))

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  main()
