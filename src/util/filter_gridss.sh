#!/usr/bin/env bash

for f in ./out/*.gridss.vcf; do
  s=${f/.gridss.vcf/}
  bcftools view -i 'QUAL>1000 & AS>0 & RAS>0' < $f > $s.gridss.high.vcf
done
