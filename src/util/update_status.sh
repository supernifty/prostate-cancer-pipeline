#!/usr/bin/env bash

set -e

ROOT=/scratch/VR0211/pan-prostate

executor=$(hostname)

while true; do
  echo "looking..."
  python $ROOT/src/util/generate_status.py > status.$$
  python $ROOT/src/util/generate_timing.py $executor > timing.$$
  scp -i ~/.ssh/peter.pem status.$$ ubuntu@htsdb.org:/home/ubuntu/src/metadata-db/status
  scp -i ~/.ssh/peter.pem timing.$$ ubuntu@htsdb.org:/home/ubuntu/src/metadata-db/timing
  echo "sleeping..."
  sleep 3600
done
