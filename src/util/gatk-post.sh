#!/bin/bash
#SBATCH --job-name=gatk-post
#SBATCH --account VR0211
#SBATCH --reservation VR0211
#SBATCH --mem=32G
#SBATCH --time=80:00:00
#SBATCH --ntasks=16
#SBATCH --nodes=1
#SBATCH -p main

set -e

module load java/1.8.0_101
module load R-gcc/3.4.0

ROOT=/scratch/VR0211/pan-prostate
BUNDLE=$ROOT/tools/gatk-bundle
GATK=$ROOT/tools/GenomeAnalysisTK-3.7.0.jar
REFERENCE=$ROOT/reference-wgs-1.1.2/core_ref_GRCh37d5/genome.fa
OUTDIR=$ROOT/out/gatk

mkdir -p $OUTDIR
cd $OUTDIR

echo "starting catvariants at $(date)"
java -cp $GATK \
     org.broadinstitute.gatk.tools.CatVariants \
     -R $REFERENCE \
     VARIANT_LIST \
     -out $OUTDIR/joint.vcf

echo "starting vqsr at $(date)"
java -jar $GATK \
        -T VariantRecalibrator \
        -nt 16 \
        -R $REFERENCE \
        -input $OUTDIR/joint.vcf \
        -recalFile $OUTDIR/joint.SNP.recal \
        -tranchesFile $OUTDIR/joint.SNP.tranches \
        -resource:hapmap,known=false,training=true,truth=true,prior=15.0 $BUNDLE/hapmap_3.3.b37.vcf.bgz \
        -resource:omni,known=false,training=true,truth=true,prior=12.0 $BUNDLE/1000G_omni2.5.b37.vcf.bgz \
        -resource:1000G,known=false,training=true,truth=false,prior=10.0 $BUNDLE/1000G_phase1.snps.high_confidence.b37.vcf.bgz \
        -resource:dbsnp,known=true,training=false,truth=false,prior=2.0 $BUNDLE/dbsnp_138.b37.vcf.bgz \
        -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR -an DP -an InbreedingCoeff \
        -tranche 100.0 -tranche 99.9 -tranche 99.0 -tranche 90.0 \
        -rscriptFile $OUTDIR/joint.recalibrate_SNP_plots.R \
        -mode SNP

echo "starting applyrecal at $(date)"
java -jar $GATK \
     -T ApplyRecalibration \
     -R $REFERENCE \
     -input $OUTDIR/joint.vcf \
     -tranchesFile $OUTDIR/joint.SNP.tranches \
     -recalFile $OUTDIR/joint.SNP.recal \
     -o $OUTDIR/joint.SNP.recal.vcf \
     --ts_filter_level 99.9 \
     --excludeFiltered \
     -mode SNP

echo "starting indel vqsr at $(date)"
java -jar $GATK \
        -T VariantRecalibrator \
        -nt 16 \
        -R $REFERENCE \
        -input $OUTDIR/joint.SNP.recal.vcf \
        -recalFile $OUTDIR/joint.indel.recal \
        -tranchesFile $OUTDIR/joint.indel.tranches \
        -resource:mills,known=false,training=true,truth=true,prior=12.0 $BUNDLE/Mills_and_1000G_gold_standard.indels.b37.vcf.bgz \
        -resource:dbsnp,known=true,training=false,truth=false,prior=2.0 $BUNDLE/dbsnp_138.b37.vcf.bgz \
        -an QD -an DP -an FS -an SOR -an ReadPosRankSum -an MQRankSum -an InbreedingCoeff \
        -tranche 100.0 -tranche 99.9 -tranche 99.0 -tranche 90.0 \
        --maxGaussians 4 \
        -rscriptFile $OUTDIR/joint.recalibrate_INDEL_plots.R \
        -mode INDEL

echo "starting indel applyrecal at $(date)"
java -Xmx15g -Djava.io.tmpdir=$ROOT/tmp \
           -jar $GATK \
           -T ApplyRecalibration \
           -R $REFERENCE \
           -input $OUTDIR/joint.SNP.recal.vcf \
           -tranchesFile $OUTDIR/joint.indel.tranches \
           -recalFile $OUTDIR/joint.indel.recal \
           -o $OUTDIR/joint.SNP.indel.recal.vcf \
           --ts_filter_level 99.9 \
           --excludeFiltered \
           -mode INDEL

echo "starting genotype refinement at $(date)"
java -jar $GATK \
        -R $REFERENCE \
        -T CalculateGenotypePosteriors \
        --supporting $BUNDLE/1000G_phase3_v4_20130502.sites.vcf.gz \
        -V $OUTDIR/joint.SNP.indel.recal.vcf \
        -o $OUTDIR/joint.SNP.indel.recal.postCGP.vcf

java -jar $GATK \
        -T LeftAlignAndTrimVariants \
        -R $REFERENCE \
        -V $OUTDIR/joint.SNP.indel.recal.postCGP.vcf \
        -o $OUTDIR/joint.SNP.indel.recal.postCGP.aln_trim_split.vcf \
        --splitMultiallelics

echo "finished at $(date)"
# run this after joint genotyping has run on all chromosomes
