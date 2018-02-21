# usage: Rscript HMMcopy.R --out_dir dir --normal normal.wig --tumor tumor.wig


# installation
#install.packages('optparse', repos = "http://cran.us.r-project.org")
source("https://bioconductor.org/biocLite.R")
#biocLite("HMMcopy")

# load libraries
library ('HMMcopy');
library ('optparse');

### command line parameters 
option_list <- list(make_option('--normal', type = 'character', default = NULL, help = 'normal wig file', metavar = 'character'), 
                    make_option('--tumor', type = 'character', default = NULL, help = 'tumor wig file', metavar = 'character'),
                    make_option('--out_dir', type = 'character', default = NULL, help = 'output directory', metavar = 'character'),
                    make_option('--ref_dir', type = 'character', default = NULL, help = 'reference directory', metavar = 'character')
                    );

opt_parser <- OptionParser(option_list = option_list);
opt <- parse_args(opt_parser);

setwd (opt$out_dir);
normal.wig <- opt$normal;
tumor.wig <- opt$tumor;

# read in gc.wig, ma.wig and tumor/normal wigs
gc.file <- paste0(opt$ref_dir, '/ref.gc.wig');
map.file <- paste0(opt$ref_dir, '/ref.map.wig');
normal_reads <- wigsToRangedData(readfile = normal.wig, gcfile = gc.file, mapfile = map.file);
normal_copy <- correctReadcount(normal_reads);
tumor_reads <- wigsToRangedData(readfile = tumor.wig, gcfile = gc.file, mapfile = map.file);
tumor_copy <- correctReadcount(tumor_reads);
somatic_copy <- tumor_copy;
somatic_copy$copy <- tumor_copy$copy - normal_copy$copy;
param <- HMMsegment(somatic_copy, getparam = TRUE);
param$mu <- log(c(1, 1.4, 2, 2.7, 3, 4.5) / 2, 2); 
param$m <- param$mu;
param$e <- 0.9999999999999999;
param$strength <- 1e300;
somatic_segments <- HMMsegment(somatic_copy, param = param);

# save results
write.table(somatic_segments$segs, file = 'somatic_segments.txt', quote = FALSE, row.names = FALSE, sep = '\t');

# plot results
chrs <- c(1:22, 'X', 'Y');
for (i in 1:length(chrs)){
png (paste0 ('somatic.chr', chrs[i], '.cnv.plot.png'), width = 980);
cols <- stateCols();
plotSegments (somatic_copy, 
              somatic_segments, 
              pch = '.', 
              ylab = 'Tumor Copy Number', 
              xlab = 'Chromosome Position', 
              chr = chrs[i], 
              main = paste0('Chromosome ', chrs[i])
              );
legend ('topleft', c('HOMD', 'HETD', 'NEUT', 'GAIN', 'AMPL', 'HLAMP'), fill = cols, horiz = TRUE, bty = 'n', cex = 1);
dev.off();
}

