#!/bin/bash
#SBATCH --job-name=filter_mt
#SBATCH --account VR0211
#SBATCH --mem=32768
#SBATCH --time=90:00:00
#SBATCH --ntasks=16
#SBATCH --nodes=1
#SBATCH -p main

# generates mt files

set -e
set -v

module load samtools-intel/1.5

echo "starting filter_sam at $(date)"

MAX_JOBS=15
RUNNING=0

for sample in ./out/*.mapped.bam; do
  sample_out="${sample/.mapped.bam/.mt.bam}" # ./out/x.mt.bam
  sample_log="${sample/.mapped.bam/.mt.log}" # ./out/x.mt.log

  echo "starting $sample at $(date)"

  samtools view -h $sample | python ./src/util/filter_sam.py 2>$sample_log | samtools view -bS - >$sample_out &

  RUNNING=$((RUNNING+1))
  if [ "$RUNNING" = "$MAX_JOBS" ]; then
    echo "waiting for current set to finish at $(date)"
    wait
    RUNNING=0
  fi
done

wait

echo "finished filter_sam at $(date)"
