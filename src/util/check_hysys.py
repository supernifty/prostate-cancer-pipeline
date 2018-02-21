#!/usr/bin/env python

import collections
import sys

# get patient info
patient = {} # sample -> patient
normal = {} # patient -> normal
for line in open('./cfg/sample-metadata.csv', 'r'):
  fields = line.strip('\n').split(',')
  patient[fields[0]] = fields[1]
  if len(fields) > 4 and fields[4] == 'Y':
    normal[fields[1]] = fields[0]

best = {}
all_results = {}
for line in sys.stdin:
  t, n, v, c = line.strip('\n').split('\t') # t n % c
  #./out/CMHS54.hysys -> CMHS54
  t = t.split('/')[-1].split('.')[0]
  n = n.split('/')[-1].split('.')[0]
  v = float(v)
  if t not in best:
    best[t] = (n, v)
  elif v > best[t][1]:
    best[t] = (n, v)

  all_results['{},{}'.format(t, n)] = v

sys.stdout.write('Tumor\tBestNormal\tBestConcordance\tIsOK\n')
for t in sorted(best):
  expected_patient = patient[t]
  inferred_patient = patient[best[t][0]]
  if expected_patient == inferred_patient:
    sys.stdout.write('{}\t{}\t{}\t{}\n'.format(t, best[t][0], best[t][1], 'OK'))
  else:
    # find alternative
    correct_sample = normal[expected_patient]
    correct_val = all_results['{},{}'.format(t, normal[expected_patient])]
    sys.stdout.write('{}\t{}\t{}\t{}\n'.format(t, best[t][0], best[t][1], 'ERROR: expected normal is {} with concordance {}'.format(correct_sample, correct_val)))

