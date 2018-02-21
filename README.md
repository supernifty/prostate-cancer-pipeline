
This is the pan prostate pipeline installed for spartan.

# Folders

The code and working directory is /data/projects/punim0095/pan-prostate

* deploy: contains the deployed ruffus pipeline
* img: contains generated singularity images
* in: input data
* out: generated data
* reference: common reference data
* scripts: helper scripts used for testing
* src: source code for ruffus pipeline, other helper scripts and templates
* tmp: temporary files created during analysis
* tools: third party tools used in the pipeline

The data is mounted at:
* /data/punim0261/data01 - generated results
* /data/punim0261/data02 - input fastq files

The account with access is:
* punim0261

# Installation

```
git clone https://github.com/supernifty/pan-prostate
mkdir cfg deploy out tools
```

## Installing dependencies

* bedtools must be on the path
* fastqc must be on the path
* rsynced pipeline_base and ruffus

* References:
  TODO other references
  wget ftp://ftp.sanger.ac.uk/pub/cancer/dockstore/human/cytoband_GRCh37d5.txt
  wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502//ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz

```
cd tools
wget https://github.com/gt1/biobambam2/releases/download/2.0.65-release-20161130121735/biobambam2-2.0.65-release-20161130121735-x86_64-etch-linux-gnu.tar.gz
tar xvfz biobambam2-2.0.65-release-20161130121735-x86_64-etch-linux-gnu.tar.gz
wget https://github.com/broadinstitute/picard/releases/download/2.8.2/picard-2.8.2.jar
wget https://github.com/dkoboldt/varscan/releases/download/2.4.2/VarScan.v2.4.2.jar
git clone http://github.com/PapenfussLab/HaveYouSwappedYourSamples.git
wget 'https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.7-0-gcfedb67'
wget https://raw.githubusercontent.com/andyrimmer/Platypus/master/extensions/Cancer/somaticMutationDetector.py
wget https://github.com/dellytools/delly/releases/download/v0.7.7/delly_v0.7.7_CentOS5.4_x86_64bit
wget https://github.com/BoutrosLaboratory/bamql/archive/v1.4.tar.gz
mv v1.4.tar.gz bamql-v1.4.tar.gz
git clone https://github.com/shahcompbio/hmmcopy_utils
cd hmmcopy_utils
module load cmake/3.6.2
cmake .
make
```

* To build reference data:
```
mkdir -p ./reference-hmmcopy
./tools/hmmcopy_utils/bin/gcCounter -c 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y reference-wgs-1.1.2/core_ref_GRCh37d5/genome.fa > reference-hmmcopy/ref.gc.wig
```

## Installing the pipeline

```
module load Python/2.7.12-intel-2016.u3
module load slurm_drmaa/1.0.7-GCC-4.9.2

cd deploy
virtualenv venv
source ./venv/bin/activate
pip install -U pip
pip install ../tools/ruffus
pip install ../tools/pipeline_base
pip install -U ../src/fastq2bam_pipeline/
pip install plotly 
```

Also had to run on merri:
```
export DRMAA_LIBRARY_PATH=/usr/local/slurm_drmaa/1.0.7-gcc/lib/libdrmaa.so
```

Also had to run on barcoo:
```
module load python-gcc/2.7.5
export DRMAA_LIBRARY_PATH=/usr/local/slurm_drmaa/1.0.7-gcc/lib/libdrmaa.so
module load samtools-intel/1.5

```
cp ../src/util/pipeline.config .
```

snowy:
```
module load Python/2.7.12-vlsci_intel-2015.08.25
module load slurm_drmaa-gcc/1.0.7
```

* Edit src/fastq2bam/src/config.py

# Inputs

* ROOT/cfg/sample-metadata.csv contains sample metadata of the form: 
```
Sample UUID,Patient UUID,Lab ID,tissue_id,is_normal,Status,Pre-aligned,Validated
CMHS1,CMHP1,299bT,BT,N,,,
```

To add new samples to the pipeline:
* If it's not already in the metadata, update ROOT/cfg/sample-metadata.csv and ROOT/cfg/uuid_map
* Run ./src/util/make_symlinks.sh (see below)
* Update ./deploy/pipeline.config (see below)

## Multiple input runs for the same sample

* Edit uuid_map and add samplename-1,filename_additional

## Symlinks

* pipeline.config expects the fastq inputs to be in the out directory.
* generate symlinks to the actual input files.

```
./src/util/make_symlinks.sh
```

This generates a *sources* file containing all fastq files, then uses ./cfg/uuid_map to convert these files to UUIDs.

A *links* file is created, which can be executed in the out directory to generate all symlinks.
```
cd out
bash ROOT/links-YYYYMMDD.sh
```

# Running the pipeline

* root is set to ROOT='/data/projects/punim0095/pan-prostate' in config.py and fastq2bam.py
* copy src/util/pipeline.config deploy/
* edit deploy/pipeline.config to include all the samples. Use links-YYYYMMDD.sh to get the list.

```
cd deploy
. ../src/util/env.sh
fastq2bam_pipeline --config pipeline.config.mini.180213 --verbose 3 --jobs 10 --use_threads --log_file ./mini`date +%Y%m%d`.log --checksum_file_name ./ruffus.sqlite.mini
--just_print # to see what will happen
--recreate_database # to rebuild what needs to run
```

# Components

* img/cgpqc.img: runs a validation script
* img/cgpmap.img: aligns the pre-aligned bam

# TODO

# Notes

## Updating htsdb.org
* cd /data/punim0261/data02/original_data/
* find -L . -name \*.fastq.gz > all-files-$(date +%Y-%m-%d).txt
* find -L . -type f -name \*.fastq.gz -print0 | xargs -0 stat --format '%n,%s' > file-sizes-$(date +%Y-%m-%d).txt

## Converting the docker container to run bwa alignment to a singularity container

Steps to building the singularity image:
Locally:
```
git clone https://github.com/cancerit/dockstore-cgpmap
git checkout master
docker build -t cgpmap .
docker run -it cgpmap:latest bash
docker ps
docker export adoring_blackwell > cgpmap.export.tar
singularity create cgpmap.img
singularity import cgpmap.img cgpmap.export.tar
```

Running the singularity image:
```
module load Singularity
```

A docker command from nectar:
docker run -i --volume=/mnt/vicnode_nfs/jobs/fastq2bam/./datastore/launcher-9b14e477-c989-4ee8-9685-c83057055ad5/inputs/35bba1e6-0503-441b-9805-ea787d38708b/bwa_idx_GRCh37d5.tar.gz:/var/lib/cwl/stg0185577a-0938-4c49-9a54-d68e7869850b/bwa_idx_GRCh37d5.tar.gz:ro --volume=/mnt/vicnode_nfs/jobs/fastq2bam/./datastore/launcher-9b14e477-c989-4ee8-9685-c83057055ad5/inputs/93494ef6-d851-405a-9ccc-624aa721385b/CMHS231.bam:/var/lib/cwl/stg495d3698-e127-4365-989b-16794e2a0060/CMHS231.bam:ro --volume=/mnt/vicnode_nfs/jobs/fastq2bam/./datastore/launcher-9b14e477-c989-4ee8-9685-c83057055ad5/inputs/06404b25-e971-4a5b-8ac3-fd7d6aa6ddb6/core_ref_GRCh37d5.tar.gz:/var/lib/cwl/stgcf238f68-053e-46e0-854a-8dbdc0f7cc00/core_ref_GRCh37d5.tar.gz:ro --volume=/mnt/vicnode_nfs/dockstore-tmp/ba232dd7-037c-48fa-9dbd-55d2061ddce6-8b4e45d8-3e6b-47cf-a7cf-e41d198938ce/tmpWk0CbJ:/var/spool/cwl:rw --volume=/mnt/vicnode_nfs/jobs/fastq2bam/datastore/launcher-9b14e477-c989-4ee8-9685-c83057055ad5/working_kf81v:/tmp:rw --workdir=/var/spool/cwl --read-only=true --user=1000 --rm --env=TMPDIR=/tmp --env=HOME=/var/spool/cwl quay.io/wtsicgp/dockstore-cgpmap:2.0.0 /opt/wtsi-cgp/bin/ds-wrapper.pl -reference /var/lib/cwl/stgcf238f68-053e-46e0-854a-8dbdc0f7cc00/core_ref_GRCh37d5.tar.gz -bwa_idx /var/lib/cwl/stg0185577a-0938-4c49-9a54-d68e7869850b/bwa_idx_GRCh37d5.tar.gz -sample ba232dd7-037c-48fa-9dbd-55d2061ddce6 -scramble  -bwa  -Y -K 100000000 -t 4 /var/lib/cwl/stg495d3698-e127-4365-989b-16794e2a0060/CMHS231.bam

## finding intermediate files to remove
```
cd /data/punim0261/data01
python ROOT/src/util/remove_intermediate_files.py
```
This generates a list of candidates. Used sed or vi to make a shell script of files and remove them.



## ruffus pipeline to run pre-alignment and alignment

