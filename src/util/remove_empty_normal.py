#!/usr/bin/env python

import sys

tp = set()
l = []
n = []
for line in sys.stdin:
  f = line.strip('\n').split(',')
  if f[1] == 'Tumor':
    tp.add(f[-1])
    sys.stdout.write(line)
  else:
    n.append(line)

for line in n:
  f = line.strip('\n').split(',')
  if f[-1] in tp:
    sys.stdout.write(line)
  else:
    sys.stderr.write('skipping ' + line) 
