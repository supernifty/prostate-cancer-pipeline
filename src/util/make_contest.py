
import os

patients = {} # sample -> patient
normals = {} # patient -> normal

#Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
for line in open('cfg/sample-metadata.csv'):
  f = line.strip('\n').split(',')
  patients[f[0]] = f[1]
  if f[4] == 'Y':
    normals[f[1]] = f[0]
  

template = open('src/util/contest.sh.template', 'r').read()
root = '/scratch/VR0211/pan-prostate'

for tumour in open('tumours_oicr.txt', 'r'):
  tumour = tumour.strip()
  patient = patients[tumour]
  normal = normals[patient]
  instance = template.replace('TUMOUR', tumour).replace('ROOT', root).replace('NORMAL', normal)
  with open('./tmp/contest/{tumour}.sh'.format(tumour=tumour), 'w') as fh:
    fh.write(instance)
