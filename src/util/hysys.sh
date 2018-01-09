#!/bin/bash
#SBATCH --job-name=hysys
#SBATCH --account VR0211
#SBATCH --mem=131072
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH -p main

set -o errexit

module load bedtools-intel/2.27.1

echo "starting at $(date)..."
python src/util/hysys.py < ./cfg/sample-metadata.csv
echo "done at $(date)"
