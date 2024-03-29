#!/usr/bin/env python

import os
import os.path
import sys

# >1 dna:chromosome chromosome:GRCh37:1:1:249250621:1
# >2 dna:chromosome chromosome:GRCh37:2:1:243199373:1
# >3 dna:chromosome chromosome:GRCh37:3:1:198022430:1
# >4 dna:chromosome chromosome:GRCh37:4:1:191154276:1
# >5 dna:chromosome chromosome:GRCh37:5:1:180915260:1
# >6 dna:chromosome chromosome:GRCh37:6:1:171115067:1
# >7 dna:chromosome chromosome:GRCh37:7:1:159138663:1
# >8 dna:chromosome chromosome:GRCh37:8:1:146364022:1
# >9 dna:chromosome chromosome:GRCh37:9:1:141213431:1
# >10 dna:chromosome chromosome:GRCh37:10:1:135534747:1
# >11 dna:chromosome chromosome:GRCh37:11:1:135006516:1
# >12 dna:chromosome chromosome:GRCh37:12:1:133851895:1
# >13 dna:chromosome chromosome:GRCh37:13:1:115169878:1
# >14 dna:chromosome chromosome:GRCh37:14:1:107349540:1
# >15 dna:chromosome chromosome:GRCh37:15:1:102531392:1
# >16 dna:chromosome chromosome:GRCh37:16:1:90354753:1
# >17 dna:chromosome chromosome:GRCh37:17:1:81195210:1
# >18 dna:chromosome chromosome:GRCh37:18:1:78077248:1
# >19 dna:chromosome chromosome:GRCh37:19:1:59128983:1
# >20 dna:chromosome chromosome:GRCh37:20:1:63025520:1
# >21 dna:chromosome chromosome:GRCh37:21:1:48129895:1
# >22 dna:chromosome chromosome:GRCh37:22:1:51304566:1
# >X dna:chromosome chromosome:GRCh37:X:1:155270560:1
# >Y dna:chromosome chromosome:GRCh37:Y:2649521:59034049:1
# >MT gi|251831106|ref|NC_012920.1| Homo sapiens mitochondrion, complete genome
# >GL000207.1 dna:supercontig supercontig::GL000207.1:1:4262:1
# >GL000226.1 dna:supercontig supercontig::GL000226.1:1:15008:1
# >GL000229.1 dna:supercontig supercontig::GL000229.1:1:19913:1
# >GL000231.1 dna:supercontig supercontig::GL000231.1:1:27386:1
# >GL000210.1 dna:supercontig supercontig::GL000210.1:1:27682:1
# >GL000239.1 dna:supercontig supercontig::GL000239.1:1:33824:1
# >GL000235.1 dna:supercontig supercontig::GL000235.1:1:34474:1
# >GL000201.1 dna:supercontig supercontig::GL000201.1:1:36148:1
# >GL000247.1 dna:supercontig supercontig::GL000247.1:1:36422:1
# >GL000245.1 dna:supercontig supercontig::GL000245.1:1:36651:1
# >GL000197.1 dna:supercontig supercontig::GL000197.1:1:37175:1
# >GL000203.1 dna:supercontig supercontig::GL000203.1:1:37498:1
# >GL000246.1 dna:supercontig supercontig::GL000246.1:1:38154:1
# >GL000249.1 dna:supercontig supercontig::GL000249.1:1:38502:1
# >GL000196.1 dna:supercontig supercontig::GL000196.1:1:38914:1
# >GL000248.1 dna:supercontig supercontig::GL000248.1:1:39786:1
# >GL000244.1 dna:supercontig supercontig::GL000244.1:1:39929:1
# >GL000238.1 dna:supercontig supercontig::GL000238.1:1:39939:1
# >GL000202.1 dna:supercontig supercontig::GL000202.1:1:40103:1
# >GL000234.1 dna:supercontig supercontig::GL000234.1:1:40531:1
# >GL000232.1 dna:supercontig supercontig::GL000232.1:1:40652:1
# >GL000206.1 dna:supercontig supercontig::GL000206.1:1:41001:1
# >GL000240.1 dna:supercontig supercontig::GL000240.1:1:41933:1
# >GL000236.1 dna:supercontig supercontig::GL000236.1:1:41934:1
# >GL000241.1 dna:supercontig supercontig::GL000241.1:1:42152:1
# >GL000243.1 dna:supercontig supercontig::GL000243.1:1:43341:1
# >GL000242.1 dna:supercontig supercontig::GL000242.1:1:43523:1
# >GL000230.1 dna:supercontig supercontig::GL000230.1:1:43691:1
# >GL000237.1 dna:supercontig supercontig::GL000237.1:1:45867:1
# >GL000233.1 dna:supercontig supercontig::GL000233.1:1:45941:1
# >GL000204.1 dna:supercontig supercontig::GL000204.1:1:81310:1
# >GL000198.1 dna:supercontig supercontig::GL000198.1:1:90085:1
# >GL000208.1 dna:supercontig supercontig::GL000208.1:1:92689:1
# >GL000191.1 dna:supercontig supercontig::GL000191.1:1:106433:1
# >GL000227.1 dna:supercontig supercontig::GL000227.1:1:128374:1
# >GL000228.1 dna:supercontig supercontig::GL000228.1:1:129120:1
# >GL000214.1 dna:supercontig supercontig::GL000214.1:1:137718:1
# >GL000221.1 dna:supercontig supercontig::GL000221.1:1:155397:1
# >GL000209.1 dna:supercontig supercontig::GL000209.1:1:159169:1
# >GL000218.1 dna:supercontig supercontig::GL000218.1:1:161147:1
# >GL000220.1 dna:supercontig supercontig::GL000220.1:1:161802:1
# >GL000213.1 dna:supercontig supercontig::GL000213.1:1:164239:1
# >GL000211.1 dna:supercontig supercontig::GL000211.1:1:166566:1
# >GL000199.1 dna:supercontig supercontig::GL000199.1:1:169874:1
# >GL000217.1 dna:supercontig supercontig::GL000217.1:1:172149:1
# >GL000216.1 dna:supercontig supercontig::GL000216.1:1:172294:1
# >GL000215.1 dna:supercontig supercontig::GL000215.1:1:172545:1
# >GL000205.1 dna:supercontig supercontig::GL000205.1:1:174588:1
# >GL000219.1 dna:supercontig supercontig::GL000219.1:1:179198:1
# >GL000224.1 dna:supercontig supercontig::GL000224.1:1:179693:1
# >GL000223.1 dna:supercontig supercontig::GL000223.1:1:180455:1
# >GL000195.1 dna:supercontig supercontig::GL000195.1:1:182896:1
# >GL000212.1 dna:supercontig supercontig::GL000212.1:1:186858:1
# >GL000222.1 dna:supercontig supercontig::GL000222.1:1:186861:1
# >GL000200.1 dna:supercontig supercontig::GL000200.1:1:187035:1
# >GL000193.1 dna:supercontig supercontig::GL000193.1:1:189789:1
# >GL000194.1 dna:supercontig supercontig::GL000194.1:1:191469:1
# >GL000225.1 dna:supercontig supercontig::GL000225.1:1:211173:1
# >GL000192.1 dna:supercontig supercontig::GL000192.1:1:547496:1
# >NC_007605
# >hs37d5

CHROMOSOMES=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y', 'MT', 'GL000207.1', 'GL000226.1', 'GL000229.1', 'GL000231.1', 'GL000210.1', 'GL000239.1', 'GL000235.1', 'GL000201.1', 'GL000247.1', 'GL000245.1', 'GL000197.1', 'GL000203.1', 'GL000246.1', 'GL000249.1', 'GL000196.1', 'GL000248.1', 'GL000244.1', 'GL000238.1', 'GL000202.1', 'GL000234.1', 'GL000232.1', 'GL000206.1', 'GL000240.1', 'GL000236.1', 'GL000241.1', 'GL000243.1', 'GL000242.1', 'GL000230.1', 'GL000237.1', 'GL000233.1', 'GL000204.1', 'GL000198.1', 'GL000208.1', 'GL000191.1', 'GL000227.1', 'GL000228.1', 'GL000214.1', 'GL000221.1', 'GL000209.1', 'GL000218.1', 'GL000220.1', 'GL000213.1', 'GL000211.1', 'GL000199.1', 'GL000217.1', 'GL000216.1', 'GL000215.1', 'GL000205.1', 'GL000219.1', 'GL000224.1', 'GL000223.1', 'GL000195.1', 'GL000212.1', 'GL000222.1', 'GL000200.1', 'GL000193.1', 'GL000194.1', 'GL000225.1', 'GL000192.1', 'NC_007605', 'hs37d5')

def cmd(c):
  sys.stderr.write('starting {}...\n'.format(c))
  os.system(c)
  sys.stderr.write('finished {}\n'.format(c))
  
def main():
  samplenames = []
  for line in open('/scratch/VR0211/pan-prostate/cfg/sample-metadata.csv', 'r'):
    # Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
    # mini,minipatient,minilab,minitissue,N,testing1,testing2,testing3
    if line.startswith('#'):
      continue
    f = line.strip('\n').split(',')
    is_normal = f[4]
    samplename = f[0]
    if is_normal == 'Y' and os.path.isfile('out/{samplename}.gatk/{samplename}.g.vcf.gz'.format(samplename=samplename)):
      samplenames.append(samplename)

    variants = ' '.join(['--variant $ROOT/out/{samplename}.gatk/{samplename}.g.vcf.gz'.format(samplename=samplename) for samplename in samplenames])

  cmd('mkdir -p /scratch/VR0211/pan-prostate/out/gatk/')
  for chromosome in CHROMOSOMES:
    cmd('sed "s/CHROMOSOME/{chromosome}/; s/VARIANT_LIST/{variant_list}/g" < /scratch/VR0211/pan-prostate/src/util/gatk-joint.sh > /scratch/VR0211/pan-prostate/out/gatk/gatk-joint-{chromosome}.sh'.format(chromosome=chromosome, variant_list=variants.replace('/', '\\/').replace('$', '\\$')))
    cmd('cd /scratch/VR0211/pan-prostate/out/gatk && sbatch /scratch/VR0211/pan-prostate/out/gatk/gatk-joint-{chromosome}.sh'.format(chromosome=chromosome))

  # post script
  chromosomes = ' '.join(['--variant $OUTDIR/joint_{chromosome}.vcf'.format(chromosome=chromosome) for chromosome in CHROMOSOMES])
  cmd('sed "s/VARIANT_LIST/{variant_list}/g" < /scratch/VR0211/pan-prostate/src/util/gatk-post.sh > /scratch/VR0211/pan-prostate/out/gatk/gatk-post.sh'.format(variant_list=chromosomes.replace('/', '\\/').replace('$', '\\$')))

if __name__ == '__main__':
  main()
