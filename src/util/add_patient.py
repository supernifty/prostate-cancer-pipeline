#!/usr/bin/env python

import sys

meta = {}

for line in open('./cfg/sample-metadata.csv', 'r'):
  fields = line.strip('\n').split(',')
  meta[fields[0]] = fields[1]

for line in sys.stdin:
  fields = line.strip('\n').split(',')
  if fields[0] in meta:
    sys.stdout.write('{},{}\n'.format(line.strip('\n'), meta[fields[0]]))
  else:
    sys.stdout.write('{},Patient\n'.format(line.strip('\n')))
