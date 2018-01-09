#!/bin/bash
#SBATCH --job-name=cmhs47
#SBATCH --account VR0211
#SBATCH --mem=262144
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH -p main

set -o errexit

echo "$(date) starting..."
python src/util/match_fastqs_full.py out/CMHS47_R1.orig.fastq.gz out/CMHS47_R2.orig.fastq.gz out/CMHS47_R1.truncated.fastq out/CMHS47_R2.truncated.fastq
echo "$(date) done"
