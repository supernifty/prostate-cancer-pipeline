#!/usr/bin/env bash

SRC=/scratch/VR0211/pan-prostate/out/
DEST=peter@spartan.hpc.unimelb.edu.au:/data/projects/punim0095/pan-prostate/out/

#rsync -avzP --dry-run --include '*.mapped.bam' --exclude='*.fastq.gz' --exclude='*.bam' $SRC $DEST
#rsync -avzP --exclude='*.fastq.gz' --exclude='*.bam' $SRC $DEST
rsync -avzP --exclude='*.fastq.gz' --exclude='*.bam' $SRC $DEST
