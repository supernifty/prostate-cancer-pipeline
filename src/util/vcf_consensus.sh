#!/usr/bin/env bash

set -e

echo "mutect vcf files"
for f in out/*.mutect1.vcf; do
  g=${f/.mutect1.vcf/}
  if [ ! -f "$g.mutect1.pass.vcf" ]; then
    egrep '(^#|PASS)' < $f > $g.mutect1.pass.vcf
  fi
done

echo "caveman vcf files"
for f in out/*.caveman-1.1.2.flagged.muts.vcf; do
  g=${f/.caveman-1.1.2.flagged.muts.vcf/}
  if [ ! -f "$g.caveman.pass.vcf" ]; then
    egrep '(^#|PASS)' < $f > $g.caveman.pass.vcf
  fi
done

echo "muse vcf files"
for f in out/*.muse.vcf; do
  g=${f/.muse.vcf/}
  if [ ! -f "$g.muse.pass.vcf" ]; then
    egrep '(^#|PASS)' < $f > $g.muse.pass.vcf
  fi
done

echo "platypus vcf files"
for f in out/*.platypus.somatic.vcf; do
  g=${f/.platypus.somatic.vcf/}
  if [ ! -f "$g.platypus.somatic.pass.vcf" ]; then
    egrep '(^#|PASS)' < $f > $g.platypus.somatic.pass.vcf
  fi
done

# make consensus
for f in out/*.caveman.pass.vcf; do
  g=${f/.caveman.pass.vcf/}
  if [ -f "$g.muse.pass.vcf" ] && [ -f "$g.platypus.somatic.pass.vcf" ] && [ -f "$g.mutect1.pass.vcf" ]; then
    python ~/../shared/pgeorgeson/src/vcf_consensus/src/snv_concordance_vcf.py --minimum_concordance 2 $g.caveman.pass.vcf $g.muse.pass.vcf $g.platypus.somatic.pass.vcf $g.mutect1.pass.vcf > $g.concordance.2.vcf
    #s=${g/out\//}
    #python ~/../shared/pgeorgeson/src/vcf_consensus/src/snv_concordance.py $g.caveman.pass.vcf $g.muse.pass.vcf $g.platypus.somatic.pass.vcf $g.mutect1.pass.vcf > tmp/concordance/$s.concordance
    #python ~/../shared/pgeorgeson/src/vcf_consensus/src/snv_intersect.py --venn $g.venn.png $g.caveman.pass.vcf $g.muse.pass.vcf $g.platypus.somatic.pass.vcf $g.mutect1.pass.vcf > tmp/concordance/$s.intersect
  fi
done
