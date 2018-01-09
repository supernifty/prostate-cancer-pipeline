#!/usr/bin/env bash

set -e
echo "starting at $(date)"
#SAMPLES="CMHS52 CMHS53 CMHS54 CMHS55 CMHS64 CMHS66 CMHS67 CMHS68 CMHS69 CMHS70"
SAMPLES="CMHS101 CMHS104 CMHS105 CMHS106 CMHS107 CMHS109 CMHS110 CMHS112 CMHS113 CMHS114 CMHS118 CMHS122 CMHS124 CMHS126 CMHS128 CMHS130 CMHS131 CMHS132 CMHS134 CMHS136 CMHS138 CMHS139 CMHS140 CMHS142 CMHS144 CMHS145 CMHS147 CMHS148 CMHS150 CMHS152 CMHS153 CMHS155 CMHS156 CMHS158 CMHS160 CMHS162 CMHS163 CMHS164 CMHS166 CMHS167 CMHS169 CMHS16 CMHS171 CMHS173 CMHS175 CMHS176 CMHS178 CMHS17 CMHS180 CMHS182 CMHS183 CMHS185 CMHS187 CMHS189 CMHS191 CMHS193 CMHS195 CMHS197 CMHS199 CMHS201 CMHS203 CMHS205 CMHS207 CMHS209 CMHS211 CMHS213 CMHS215 CMHS217 CMHS219 CMHS221 CMHS223 CMHS225 CMHS227 CMHS229 CMHS231 CMHS232 CMHS233 CMHS234 CMHS236 CMHS238 CMHS240 CMHS242 CMHS244 CMHS246 CMHS248 CMHS250 CMHS252 CMHS254 CMHS256 CMHS258 CMHS260 CMHS261 CMHS263 CMHS265 CMHS267 CMHS269 CMHS271 CMHS273 CMHS275 CMHS277 CMHS279 CMHS281 CMHS283 CMHS285 CMHS287 CMHS289 CMHS291 CMHS293 CMHS295 CMHS297 CMHS299 CMHS301 CMHS303 CMHS305 CMHS307 CMHS309 CMHS311 CMHS313 CMHS315 CMHS317 CMHS319 CMHS321 CMHS323 CMHS325 CMHS327 CMHS329 CMHS331 CMHS333 CMHS335 CMHS337 CMHS339 CMHS341 CMHS343 CMHS345 CMHS347 CMHS349 CMHS351 CMHS353 CMHS355 CMHS357 CMHS359 CMHS360 CMHS362 CMHS364 CMHS366 CMHS368 CMHS36 CMHS370 CMHS372 CMHS374 CMHS376 CMHS37 CMHS39 CMHS40 CMHS42 CMHS43 CMHS45 CMHS49 CMHS52 CMHS53 CMHS54 CMHS55 CMHS58 CMHS60 CMHS62 CMHS64 CMHS66 CMHS67 CMHS68 CMHS69 CMHS70 CMHS72 CMHS73 CMHS75 CMHS76 CMHS78 CMHS79 CMHS82 CMHS83 CMHS86 CMHS87 CMHS91 CMHS92 CMHS94 CMHS96 CMHS97 CMHS98"

# find samplenames tumour then normal
for tumor in $SAMPLES; do
  tumorfirst=false
  tumorsecond=false
  echo "starting $tumor at $(date)"
  first=$(grep -m 1 '^#CHROM' < ./out/${tumor}.platypus.vcf | cut -f10)
  second=$(grep -m 1 '^#CHROM' < ./out/${tumor}.platypus.vcf | cut -f11)
  grep $first ./out/spartan/${tumor}.validation > /dev/null && tumorfirst=true
  grep $second ./out/spartan/${tumor}.validation > /dev/null && tumorsecond=true
  if [ $tumorfirst = true ]; then
    echo "tumor $tumor is first"
    python tools/platypus-extensions/somaticMutationDetector.py --inputVCF ./out/${tumor}.platypus.vcf --outputVCF ./out/${tumor}.platypus.somatic.vcf --tumourSample $first --normalSample $second --minPosterior 5
  elif [ $tumorsecond = true ]; then
    echo "tumor $tumor is second"
    python tools/platypus-extensions/somaticMutationDetector.py --inputVCF ./out/${tumor}.platypus.vcf --outputVCF ./out/${tumor}.platypus.somatic.vcf --tumourSample $second --normalSample $first --minPosterior 5
  else
    echo "WARN: failed to find $first or $second in $tumor from spartan"
    grep $first ./out/${tumor}.validation > /dev/null && tumorfirst=true
    grep $second ./out/${tumor}.validation > /dev/null && tumorsecond=true
    if [ $tumorfirst = true ]; then
      echo "tumor $tumor is first"
      python tools/platypus-extensions/somaticMutationDetector.py --inputVCF ./out/${tumor}.platypus.vcf --outputVCF ./out/${tumor}.platypus.somatic.vcf --tumourSample $first --normalSample $second --minPosterior 5
    elif [ $tumorsecond = true ]; then
      echo "tumor $tumor is second"
      python tools/platypus-extensions/somaticMutationDetector.py --inputVCF ./out/${tumor}.platypus.vcf --outputVCF ./out/${tumor}.platypus.somatic.vcf --tumourSample $second --normalSample $first --minPosterior 5
    else
      echo "ERROR: failed to find $first or $second in $tumor from barcoo"
    fi
  fi
done
echo "finished at $(date)"
