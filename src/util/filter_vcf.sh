#!/usr/bin/env bash

S="CMHS51 CMHS52 CMHS53 CMHS54 CMHS55 CMHS64 CMHS65 CMHS66 CMHS67 CMHS68 CMHS69 CMHS70 CMHS71"

for s in $S; do
  python src/util/filter_germline.py tumorfirst < ./out/CMHS52.muse.vcf > ./out/CMHS52.muse.pass.vcf
  python src/util/filter_germline.py tumorfirst < ./out/CMHS52.platypus.vcf > ./out/CMHS52.platypus.pass.vcf
  python src/util/filter_germline.py normalfirst < ./out/CMHS52.mutect1.vcf > ./out/CMHS52.mutect1.pass.vcf
  # WGS_775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52/caveman/775021c4-50ef-48e4-b9d7-bbfa959b67b4_vs_be887b7f-8cb2-418f-be9a-9c683bc79b52.annot.muts.vcf.gz
  tar xvfz ./out/CMHS52.wgs/WGS_*.result.tar.gz "*.annot.muts.vcf.gz"
  gunzip < ./WGS_*/caveman/*.annot.muts.vcf.gz | python src/util/filter_germline.py normalfirst > ./out/CMHS52.caveman.pass.vcf
  rm -r ./WGS_*;
done
