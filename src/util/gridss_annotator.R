# based on https://github.com/PapenfussLab/gridss/blob/master/example/somatic.R

# e.g.
# Rscript gridss_annotator.R ./out/MINIA52.gridss.vcf ./out/MINIA52.mapped.bam ./out/MINIA51.mapped.bam

# parameters: vcf tumour.bam normal.bam
args <- commandArgs(TRUE)
vcf_file <- args[1]
tumour_bam <- args[2]
normal_bam <- args[3]

cat('installing...\n')

#source("https://bioconductor.org/biocLite.R")
#biocLite("VariantAnnotation")

#install.packages("stringr", repos='http://cran.us.r-project.org')
#install.packages("withr", repos='http://cran.us.r-project.org')
library(withr)

#install.packages("devtools", repos='http://cran.us.r-project.org')

cat('loading...\n')
#install.packages("httr", repos='http://cran.us.r-project.org')
library(httr, lib.loc='./r-lib')
#install.packages("curl", repos='http://cran.us.r-project.org')
library(curl)

library(stringr)
library(VariantAnnotation)
library(devtools)

#install_github("PapenfussLab/StructuralVariantAnnotation")
library(StructuralVariantAnnotation)

cat('read vcf:', vcf_file, '\n')
vcf <- readVcf(vcf_file, "hg19")
cat('size', dim(vcf), '\n')

# filter out low quality calls
cat('filter vcf:', vcf_file, '\n')
vcf <- vcf[rowRanges(vcf)$FILTER %in% c(".", "PASS"),]
cat('size', dim(vcf), '\n')

# somatic calls have no support in the normal
cat('find somatic:', vcf_file, 'with', normal_bam, '...\n')
somatic_vcf <- vcf[geno(vcf)$QUAL[, normal_bam] == 0,]
cat('size', dim(somatic_vcf), '\n')

# somatic loss of heterozygosity has no support in the tumour
cat('find loh:', vcf_file,  'with', tumour_bam, '...\n')
loh_vcf <- vcf[geno(vcf)$QUAL[,tumour_bam] == 0,]
cat('size', dim(loh_vcf), '\n')

# Output BEDPE for use by circos
gr <- breakpointRanges(somatic_vcf)
bedpe <- data.frame(
    chrom1=seqnames(gr),
    start1=start(gr) - 1,
    end1=end(gr),
    chrom1=seqnames(partner(gr)),
    start1=start(partner(gr) - 1),
    end1=end(partner(gr)),
    name=names(gr),
    score=gr$QUAL,
    strand1=strand(gr),
    strand2=strand(partner(gr))
    )
# Just the lower of the two breakends so we don't output everything twice
bedpe <- bedpe[str_detect(bedpe$name, "gridss.+o"),]
write.table(bedpe, vcf_file + ".bedpe", quote=FALSE, sep='\t', row.names=FALSE, col.names=FALSE)

