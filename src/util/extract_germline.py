#!/usr/bin/env python

##################
# extract germline snps in a provided list of genes for a given germline sample
# usage:
# python extract_germline.py
##################

import collections
import logging
import os
import sys

PADDING=1000
EXONS="/scratch/VR0320/pgeorgeson/pan-prostate/reference-misc/exons.bed"
METADATA="/scratch/VR0320/pgeorgeson/pan-prostate/cfg/sample-metadata.csv"
TMP="/scratch/VR0320/pgeorgeson/pan-prostate/tmp/"
GENES=set(['IDH1', 'IDH2'])

def process():
  # get range
  genes_max = collections.defaultdict(int)
  genes_min = {}
  genes_chr = {}

  for line in open(EXONS, 'r'):
    if line.startswith('#'):
      continue
    fields = line.strip().split('\t') # chr start stop gene
    if fields[3] in GENES:
      genes_chr[fields[3]] = fields[0].replace('chr', '')
      if fields[3] not in genes_min:
        genes_min[fields[3]] = 1e10
      genes_min[fields[3]] = min(genes_min[fields[3]], int(fields[1]))
      genes_max[fields[3]] = max(genes_max[fields[3]], int(fields[2]))

  # list of samples
  # Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
  patient_tumor = collections.defaultdict(set) # patient -> tumor
  patient_normal = collections.defaultdict(set) # patient -> normal
  for line in open(METADATA, 'r'):
    fields = line.strip().split(',')
    if fields[4] == 'Y': # normal
      patient_normal[fields[1]].add(fields[0])
    else:
      patient_tumor[fields[1]].add(fields[0])

  # look at all the normals
  for patient in patient_normal:
    logging.info('Patient %s', patient)
    for normal in patient_normal[patient]:
      logging.info('Normal %s', normal)
      # find a tumour
      if len(patient_tumor[patient]) == 0:
        logging.warn('No tumour for %s', normal)
      else:
        tumour = list(patient_tumor[patient])[0]
        logging.info('Using tumour %s', tumour)

        # find the caveman file
        # it's in ./out/CMHS309.wgs/WGS_*.result.tar.gz
        # it's called ./WGS_775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52/caveman/775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52.snps.ids.vcf.gz

        # the brass file is ./WGS_775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52/brass/775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52.annot.vcf.gz
        command = 'tar xvfz ./out/{}.wgs/WGS_*.result.tar.gz "*.snps.ids.vcf.gz*" "*.annot.vcf.gz*"'.format(tumour)
        logging.info('Executing: %s...', command)
        err = os.system(command)
        if err == 0:
          logging.info('Executing: %s: done', command)
        else:
          logging.warn('Executing: %s: failed with return code %i', command, err)
          continue
        
        # filter it
        regions = ['{}:{}-{}'.format(genes_chr[gene], genes_min[gene] - PADDING, genes_max[gene] + PADDING) for gene in GENES]

        # caveman
        command = 'tabix -h ./WGS_*/caveman/*.snps.ids.vcf.gz {} > ./out/{}.caveman.filtered.vcf'.format(' '.join(regions), normal) 
        logging.info('Executing: %s...', command)
        os.system(command)
        logging.info('Executing: %s: done', command)

        # brass
        command = 'tabix -h ./WGS_*/brass/*.annot.vcf.gz {} > ./out/{}.brass.filtered.vcf'.format(' '.join(regions), normal) 
        logging.info('Executing: %s...', command)
        os.system(command)
        logging.info('Executing: %s: done', command)

        # remove files
        command = 'rm -r WGS_*/'
        logging.info('Executing: %s...', command)
        os.system(command)
        logging.info('Executing: %s: done', command)
        #sys.exit()
  

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  process()
