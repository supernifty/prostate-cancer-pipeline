#!/usr/bin/env python
#
# usage:
# python upload_analyses.py < ./cfg/upload_src.csv > ./cfg/upload_yymmdd.csv
# then move output to upload_src if ok

import collections
import logging
import os
import os.path
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

ENCRYPTION_KEY="cfg/oicr.public.key"
#TARGET_DIR="./oicr/gatk"
TARGET_DIR="/scratch/VR0211/pan-prostate/oicr"
SUFFIX="180220" # encrypted files
LIVE=True

def run(cmd, always=False):
  logging.info('{}...'.format(cmd))
  if LIVE or always:
    os.system(cmd)
  logging.info('{}: done'.format(cmd))

def upload(filename):
  '''
  '''
  #TODO
  
def encrypt(files, target):
  if len(files) > 0:
    # tar all files
    run("cd out && tar cfz {target_dir}/{target}.tgz {infiles} 1>&2".format(target=target, target_dir=TARGET_DIR, infiles=' '.join(files)))
    run("md5sum {target_dir}/{target}.tgz > {target_dir}/{target}.tgz.md5".format(target_dir=TARGET_DIR, target=target))
    run("openssl enc -aes-256-cbc -salt -in {target_dir}/{target}.tgz -out {target_dir}/{target}.tgz.enc -pass file:./cfg/oicr.encryption.key".format(target_dir=TARGET_DIR, target=target))

# only run once!
#run("openssl rand -base64 32 -out ./cfg/oicr.encryption.key")
#run("openssl rsautl -encrypt -inkey {key} -pubin -in ./cfg/oicr.encryption.key -out {target_dir}/encryption.key.enc".format(target_dir=TARGET_DIR, key=ENCRYPTION_KEY))
# TODO upload encryption.key.enc

# get gatk results
run('gunzip < ./out/gatk/joint.SNP.indel.recal.postCGP.aln_trim_split.vcf.gz | grep -m 1 "^##GATKCommandLine.GenotypeGVCFs" > ./oicr/tmp', always=True)
gatk_samples = open('./oicr/tmp', 'r').read()

first = True
counts = collections.defaultdict(int)
files = collections.defaultdict(list)
for line in sys.stdin:
  if first:
    sys.stdout.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format('Sample', 'Type', 'MT', 'mutect1', 'hmmcopy', 'delly', 'gatk', 'contest', 'sniper', 'callable', 'pindel', 'hmmcopy_wig', 'patient', 'uuid'))
    first = False
    continue
  fields = line.strip('\n').split(',')
  # sampleid,sampletype
  result = {}
  result['uuid'] = ''

  # MT Filter (2),Mutect1 (3),HMMCopy (4),Delly (5),GATK (6),ContEst (7),SomaticSniper (8),CallableBases (9),Pindel (10), wig (11)
  result['mt'] = fields[2] or 'TODO' # barcoo
  filename = '{sample}.mt.bam'.format(sample=fields[0])
  full = './out/{}'.format(filename)
  if result['mt'] != 'Uploaded' and os.path.isfile(full):
    counts['mt'] += 1
    counts['mt_size'] += os.stat(full).st_size
    result['mt'] = 'Uploaded'.format(os.stat(full).st_size) # available
    files['mt'].append(filename)
   
  result['contest'] = fields[7] or 'TODO' # not run
  filename = '{sample}.contest.txt'.format(sample=fields[0])
  full = './out/{}'.format(filename)
  if result['contest'] != 'Uploaded' and os.path.isfile(full):
    counts['contest'] += 1
    counts['contest_size'] += os.stat(full).st_size
    result['contest'] = 'Uploaded'.format(os.stat(full).st_size) # available
    files['contest'].append(filename)
 
  result['callable'] = fields[9] or 'TODO' # not run
  filename = '{sample}.callable.bed'.format(sample=fields[0])
  full = './out/{}'.format(filename)
  if result['callable'] != 'Uploaded' and os.path.isfile(full):
    counts['callable'] += 1
    counts['callable_size'] += os.stat(full).st_size
    result['callable'] = 'Uploaded'.format(os.stat(full).st_size) # available
    files['callable'].append(filename)

  result['hmmcopy'] = fields[4] or 'TODO' # barcoo
  filename = '{sample}.hmmcopy'.format(sample=fields[0])
  full = './out/{}/somatic_segments.txt'.format(filename)
  if result['hmmcopy'] != 'Uploaded' and os.path.isfile(full):
    counts['hmmcopy'] += 1
    counts['hmmcopy_size'] += os.stat(full).st_size
    result['hmmcopy'] = 'Uploaded'.format(os.stat(full).st_size) # available
    files['hmmcopy'].append(filename)

  full = './out/{}/normal_segments.txt'.format(filename)
  if result['hmmcopy'] != 'Uploaded' and os.path.isfile(full):
    counts['hmmcopy'] += 1
    counts['hmmcopy_size'] += os.stat(full).st_size
    result['hmmcopy'] = 'Uploaded'.format(os.stat(full).st_size) # available
    files['hmmcopy'].append(filename)

  result['hmmcopy_wig'] = fields[11] or 'TODO' # barcoo
  filename = '{sample}.mapped.bam.wig'.format(sample=fields[0])
  full = './out/{}'.format(filename)
  if result['hmmcopy_wig'] != 'Uploaded' and os.path.isfile(full):
    counts['hmmcopy_wig'] += 1
    counts['hmmcopy_wig_size'] += os.stat(full).st_size
    result['hmmcopy_wig'] = 'Uploaded'.format(os.stat(full).st_size) # available
    files['hmmcopy_wig'].append(filename)
 
  # tumour specific
  if fields[1].lower() == 'tumor':
    result['mutect1'] = fields[3] or 'TODO' # available
    #result['mutect1'] = 'TODO' # available (forces all to be included)
    filename = '{sample}.mutect1.pass.vcf'.format(sample=fields[0])
    full = './out/{}'.format(filename)
    if result['mutect1'] != 'Uploaded' and os.path.isfile(full):
      counts['mutect1'] += 1
      counts['mutect1_size'] += os.stat(full).st_size
      result['mutect1'] = 'Uploaded'.format(os.stat(full).st_size) # available
      files['mutect1'].append(filename)
 
 
    result['delly'] = fields[5] or 'TODO' # barcoo
    filename = '{sample}.delly.vcf'.format(sample=fields[0])
    full = './out/{}'.format(filename)
    if result['delly'] != 'Uploaded' and os.path.isfile(full):
      counts['delly'] += 1
      counts['delly_size'] += os.stat(full).st_size
      result['delly'] = 'Uploaded'.format(os.stat(full).st_size) # available
      files['delly'].append(filename)

    result['sniper'] = fields[8] or 'TODO' # not run

    # pindel ./out/CMHS189.pindel-1.1.2.vcf.gz
    result['pindel'] = fields[10] or 'TODO'
    filename = '{sample}.pindel-1.1.2.vcf.gz'.format(sample=fields[0])
    full = './out/{}'.format(filename)
    if result['pindel'] != 'Uploaded' and os.path.isfile(full):
      counts['pindel'] += 1
      counts['pindel_size'] += os.stat(full).st_size
      result['pindel'] = 'Uploaded'.format(os.stat(full).st_size) # available
      files['pindel'].append(filename)

    result['gatk'] = 'N/A' 

    counts['tumor'] += 1

  # normal specific
  if fields[1].lower() == 'normal':
    result['gatk'] = fields[6] or 'TODO' # not available
    filename = '{sample}.g.vcf.gz'.format(sample=fields[0])
    if result['gatk'] != 'Uploaded' and filename in gatk_samples:
      counts['gatk'] += 1
      result['gatk'] = 'Uploaded' # available
      # write out sample id
      v = open("./out/{sample}.validation".format(sample=fields[0]), 'r').readlines()
      uid = v[1].split('\t')[8]
      result['uuid'] = uid

    result['mutect1'] = 'N/A'
    result['delly'] = 'N/A'
    result['sniper'] = 'N/A'
    result['pindel'] = 'N/A'

    counts['normal'] += 1

  counts['total'] += 1
  sys.stdout.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(fields[0], fields[1], result['mt'], result['mutect1'], result['hmmcopy'], result['delly'], result['gatk'], result['contest'], result['sniper'], result['callable'], result['pindel'], result['hmmcopy_wig'], fields[12], result['uuid']))

encrypt(files['hmmcopy'], 'hmmcopy_{}'.format(SUFFIX))
encrypt(files['hmmcopy_wig'], 'hmmcopy_wig_{}'.format(SUFFIX))
encrypt(files['mt'], 'mt_{}'.format(SUFFIX))
encrypt(files['mutect1'], 'mutect1_{}'.format(SUFFIX))
encrypt(files['pindel'], 'pindel_{}'.format(SUFFIX))
encrypt(files['callable'], 'callable_{}'.format(SUFFIX))
encrypt(files['contest'], 'contest_{}'.format(SUFFIX))
encrypt(files['delly'], 'delly_{}'.format(SUFFIX))
# gatk to be done manually

logging.info('{}'.format(counts))
