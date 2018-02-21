#!/usr/bin/env python

# usage:
# samtools view -h orig.bam | python filter_sam.py | samtools view -bS > filtered.bam
#
# implemented rule:
#   (chr(M) & mate_chr(M)) | (chr(Y) & after(59000000) & mate_chr(M))

# ST-E00129:538:HGC55ALXX:4:1101:14093:2628       129     1       10392   3       76M75S  7       159128568       0       CCTAACCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCCTACCCCTAACCCTAACCCCAACCCCGCCCCCTAACCCTAACCCGAACCCGTACCCCAACCCCAAACCCAAACCCCAACCAAAAGCCCACCCCCCGACCC AAFFFJJJJJJJJJJJJJJJJJF<7A7F<F<-AF<FFJJ--F<FF--F<J<7-77-AJ<------<A<FJ---7<---7-77--7-------7-7A--77F7-77<---7-------7F<--7-77-F-7<-----77<<--7----)AFF NM:i:2  MD:Z:54A15T5    AS:i:66 XS:i:62 RG:Z:MINIA52-HGC55ALXX-GAATTCGT.4
# ST-E00129:538:HGC55ALXX:4:1102:17807:14758      99      1       11743   0       151M    =       12049   457     TGATGATTTTGCTGCATGGCCGGTGTTGAGAATGACTGCGCAAATTTGCCGGATTTCCTTTGCTGTTCCTGCATGTAGTTTAAACGAGATTGCCAGCACCGGGTATCATTCACCATTTTTCTTTTCGTTAACTTGCCGTCAGCCTTTTCTT AAFFFFFJJJJJJJJJJJJJJJJAJFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJJFJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ<JJJ7JJFJJF NM:i:0  MD:Z:151        AS:i:151        XS:i:151        RG:Z:MINIA52-HGC55ALXX-GAATTCGT.4
# ST-E00129:538:HGC55ALXX:4:1102:17807:14758      147     1       12049   0       151M    =       11743   -457    CAAGCTGAGCACTGGAGTGTAGTTTTCCTGTGGAGAGGAGCCATGCCTAGAGTGGGATGGGCCATTGTTCATCTTCTGGCCCCTGTTGTCTGCATGTAACTTAATACCACAACCAGGCATAGGGGAAAGATTGGAGGAAAGATGAGTGACA FJFJJJJ7FF7AJFJ<F-F7JFJ7FJFFFJJJJJJJJJ<AAJJFJJJJFJJJJJ<JFJJJJFFJFJJJJJJFJAF7JFA7-7<JJJJF7JJJJJJJJJJJJJJFFAFJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFFFAA NM:i:2  MD:Z:19G129G1   AS:i:144        XS:i:144        RG:Z:MINIA52-HGC55ALXX-GAATTCGT.4

# bamql -b -o output.bam -f input.bam ' (chr(M) & mate_chr(M)) | (chr(Y) & after(59000000) & mate_chr(M))

import collections
import logging
import sys

def ok(fields, counts):
  # 2 = chrom
  # 3 = position
  # 6 = mate chrom

  # chr(M) & mate_chr(M)
  if fields[2] == 'MT' and (fields[6] == '=' or fields[6] == 'MT'):
    counts['accept'] += 1
    counts['accept_{}_{}'.format(fields[2], fields[6])] += 1
    return True

  # (chr(Y) & after(59000000) & mate_chr(M)
  if fields[2] == 'Y' and fields[6] == 'MT' and int(fields[3]) >= 59000000:
    counts['accept'] += 1
    counts['accept_{}_{}'.format(fields[2], fields[6])] += 1
    return True

  counts['reject'] += 1
  counts['reject_{}_{}'.format(fields[2], fields[6])] += 1
  #counts['reject_{}'.format(fields[2])] += 1
  return False

def main():
  counts = collections.defaultdict(int)
  idx = 0
  for idx, line in enumerate(sys.stdin):
  
    if line.startswith('@'):
      sys.stdout.write(line)
      continue
  
    fields = line.strip('\n').split('\t')

    if ok(fields, counts):
      sys.stdout.write(line)
    else:
      pass

    if idx < 1000000 and idx % 100000 == 0 or idx % 1000000 == 0:
      logging.info('%i lines processed. %i/%i.', idx, counts['accept'], counts['reject'])

  logging.info('wrote %i total. Stats:\n%s', idx + 1, '\n'.join(['{}\t{}'.format(k, counts[k]) for k in sorted(counts)]))

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  main()
