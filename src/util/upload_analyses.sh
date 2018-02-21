#!/bin/bash
#SBATCH --job-name=encrypt_gatk
#SBATCH --account VR0211
#SBATCH --mem=32768
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH -p main

set -o errexit

python src/util/upload_analyses.py < ./cfg/upload_src.csv > ./cfg/upload_updated_$(date +%Y%m%d).csv
