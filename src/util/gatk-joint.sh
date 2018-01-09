#!/bin/bash
#SBATCH --job-name=CHROMOSOME-hc
#SBATCH --account VR0211
#SBATCH --reservation VR0211
#SBATCH --mem=32G
#SBATCH --time=80:00:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH -p main

set -e

module load java/1.8.0_101

ROOT=/scratch/VR0320/pgeorgeson/pan-prostate
BUNDLE=$ROOT/tools/gatk-bundle
GATK=$ROOT/tools/GenomeAnalysisTK-3.7.0.jar
REFERENCE=$ROOT/reference-wgs-1.1.2/core_ref_GRCh37d5/genome.fa
OUTDIR=$ROOT/out/gatk

mkdir -p $OUTDIR

echo "starting genotyping for CHROMOSOME at $(date)"
java -Xmx30G -jar $GATK \
     -T GenotypeGVCFs \
     -R $REFERENCE \
     --dbsnp $BUNDLE/dbsnp_138.b37.vcf.bgz \
     VARIANT_LIST \
     -L CHROMOSOME \
     -newQual \
     --disable_auto_index_creation_and_locking_when_reading_rods \
     -o $OUTDIR/joint_CHROMOSOME.vcf 

echo "finished genotyping CHROMOSOME at $(date)"
