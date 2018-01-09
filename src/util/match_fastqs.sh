#!/bin/bash
#SBATCH --job-name=cmhs47
#SBATCH --account VR0211
#SBATCH --mem=8192
#SBATCH --time=08:00:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH -p main

set -o errexit

echo "$(date) starting..."
python src/util/match_fastqs.py out/CMHS47_R1.orig.fastq.gz out/CMHS47_R2.orig.fastq.gz out/CMHS47_R1.truncated.fastq out/CMHS47_R2.truncated.fastq
echo "$(date) gzipping R1"
gzip out/CMHS47_R1.truncated.fastq
echo "$(date) gzipping R2"
gzip out/CMHS47_R2.truncated.fastq
echo "$(date) done"
