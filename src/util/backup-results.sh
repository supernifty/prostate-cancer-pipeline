#!/usr/bin/env bash

SRC=/scratch/VR0211/pan-prostate/out/
DEST=/vlsci/VR0211/shared/pgeorgeson/out/

rsync -avzP --dry-run --include '*.mapped.bam' --exclude='*.fastq.gz' --exclude='*.bam' $SRC $DEST
#rsync -avzP --exclude='*.fastq.gz' --exclude='*.bam' $SRC $DEST
