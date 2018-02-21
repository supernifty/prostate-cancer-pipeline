
for f in ./out/*.mutect1.vcf; do
  target=${f/.mutect1.vcf/.mutect1.pass.vcf}
  echo "$f -> $target"
  sed '/\tREJECT\t/d' < $f > $target
done
