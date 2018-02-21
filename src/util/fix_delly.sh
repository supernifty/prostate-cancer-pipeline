#!/usr/bin/env bash

for f in ./out/*.delly.completed; do
  alt=${f/.completed/.vcf}
  if [ -s $alt ]; then
    echo "skipping $f"
  else
    echo "rm $f"
    rm "$f"
  fi
done
