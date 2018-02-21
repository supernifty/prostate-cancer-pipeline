'''
Build the pipeline workflow by plumbing the stages together.
'''

from ruffus import Pipeline, suffix, formatter, add_inputs, output_from
from stages import Stages

def make_pipeline(state):
    '''Build the pipeline by constructing stages and connecting them together'''
    # Build an empty pipeline
    pipeline = Pipeline(name='fastq2bam')
    # Get a list of paths to all the FASTQ files
    input_files = state.config.get_option('files')
    # Stages are dependent on the state
    stages = Stages(state)

    # The original files
    # This is a dummy stage. It is useful because it makes a node in the
    # pipeline graph, and gives the pipeline an obvious starting point.
    pipeline.originate(
        task_func=stages.original_files,
        name='original_files',
        output=input_files)

    #
    # performs fastqc on fastq inputs
    # 
    pipeline.transform(
        task_func=stages.fastqc,
        name='fastqc',
        input=output_from('original_files'),
        filter=formatter('(?P<path>.+)/(?P<filename>.+).fastq.gz'),
        output='{path[0]}/{filename[0]}_fastqc')

    #
    # converts the fastq inputs to pre-aligned bams
    #
    pipeline.transform(
        task_func=stages.fastq2bam,
        name='fastq2bam',
        input=output_from('original_files'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+)_R1.fastq.gz'),
        add_inputs=add_inputs('{path[0]}/{sample[0]}_R2.fastq.gz'),
        extras=['{sample[0]}'],
        output='{path[0]}/{sample[0]}.bam')

    #
    # validates pre-aligned bams x.bam -> x.validation
    #
    pipeline.transform(
        task_func=stages.validate_prealigned_bam,
        name='validate_prealigned_bam',
        input=output_from('fastq2bam'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).bam'),
        output='{path[0]}/{sample[0]}.validation')

    # aligns pre-aligned bam x.bam -> x.mapped.bam
    pipeline.transform(
        task_func=stages.align,
        name='align',
        input=output_from('validate_prealigned_bam'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).validation'),
        add_inputs=add_inputs('{path[0]}/{sample[0]}.bam'),
        output='{path[0]}/{sample[0]}.mapped.bam')

    # generates stats about an aligned bam
    pipeline.transform(
        task_func=stages.align_stats_bedtools,
        name='align_stats_bedtools',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.genomecov.stats')

    # generates stats about an aligned bam
    pipeline.transform(
        task_func=stages.align_stats_picard,
        name='align_stats_picard',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.picard.stats')

    #
    # runs the Sanger variant calling pipeline
    #
    #pipeline.transform(
    #    task_func=stages.analyse_wgs,
    #    name='analyse_wgs',
    #    input=output_from('align'),
    #    filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
    #    output='{path[0]}/{sample[0]}.wgs.1.1.2/manifest')

    # runs the components of the Sanger variant calling pipeline
    pipeline.transform(
        task_func=stages.analyse_wgs_prepare,
        name='analyse_wgs_prepare',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.prepare')

    pipeline.transform(
        task_func=stages.analyse_wgs_reference_files,
        name='analyse_wgs_reference_files',
        input=[output_from('align'), output_from('analyse_wgs_prepare')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.reference_files')

    pipeline.transform(
        task_func=stages.analyse_wgs_init,
        name='analyse_wgs_init',
        input=[output_from('align'), output_from('analyse_wgs_reference_files')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.init')

    # block 1
    pipeline.transform(
        task_func=stages.analyse_wgs_verify_WT,
        name='analyse_wgs_verify_WT',
        input=[output_from('align'), output_from('analyse_wgs_init')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.verify_WT')

    #pipeline.transform(
    #    task_func=stages.analyse_wgs_cgpPindel_input,
    #    name='analyse_wgs_cgpPindel_input',
    #    input=[output_from('align'), output_from('analyse_wgs_init')],
    #    filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
    #    output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.cgpPindel_input')

    pipeline.transform(
        task_func=stages.analyse_wgs_alleleCount,
        name='analyse_wgs_alleleCount',
        input=[output_from('align'), output_from('analyse_wgs_init')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.alleleCount')

    # block 2

    pipeline.transform(
        task_func=stages.analyse_wgs_cgpPindel,
        name='analyse_wgs_cgpPindel',
        #input=[output_from('align'), output_from('analyse_wgs_cgpPindel_input')],
        input=[output_from('align'), output_from('analyse_wgs_init')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.cgpPindel')

    pipeline.transform(
        task_func=stages.analyse_wgs_BRASS_input,
        name='analyse_wgs_BRASS_input',
        input=[output_from('align'), output_from('analyse_wgs_init')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.BRASS_input')

    pipeline.transform(
        task_func=stages.analyse_wgs_BRASS_cover,
        name='analyse_wgs_BRASS_cover',
        input=[output_from('align'), output_from('analyse_wgs_init')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.BRASS_cover')

    pipeline.transform(
        task_func=stages.analyse_wgs_CaVEMan_split,
        name='analyse_wgs_CaVEMan_split',
        input=[output_from('align'), output_from('analyse_wgs_init')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.CaVEMan_split')

    # block 2.5
    pipeline.transform(
        task_func=stages.analyse_wgs_ascat,
        name='analyse_wgs_ascat',
        input=[output_from('align'), output_from('analyse_wgs_CaVEMan_split')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.ascat')

    # after block 2
    pipeline.transform(
        task_func=stages.analyse_wgs_ascat_prep,
        name='analyse_wgs_ascat_prep',
        input=[output_from('align'), output_from('analyse_wgs_ascat')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.ascat_prep')

    pipeline.transform(
        task_func=stages.analyse_wgs_pindel_prep,
        name='analyse_wgs_pindel_prep',
        input=[output_from('align'), output_from('analyse_wgs_cgpPindel')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.pindel_prep')

    # parallel block 3
    pipeline.transform(
        task_func=stages.analyse_wgs_verify_MT,
        name='analyse_wgs_verify_MT',
        input=[output_from('align'), output_from('analyse_wgs_verify_WT'), output_from('analyse_wgs_ascat_prep')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.verify_MT')

    pipeline.transform(
        task_func=stages.analyse_wgs_CaVEMan,
        name='analyse_wgs_CaVEMan',
        input=[output_from('align'), output_from('analyse_wgs_CaVEMan_split'), output_from('analyse_wgs_ascat_prep'), output_from('analyse_wgs_cgpPindel')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.CaVEMan')

    pipeline.transform(
        task_func=stages.analyse_wgs_BRASS,
        name='analyse_wgs_BRASS',
        input=[output_from('align'), output_from('analyse_wgs_BRASS_cover'), output_from('analyse_wgs_BRASS_input'), output_from('analyse_wgs_ascat_prep')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.BRASS')

    pipeline.transform(
        task_func=stages.analyse_wgs_cgpPindel_annot,
        name='analyse_wgs_cgpPindel_annot',
        input=[output_from('align'), output_from('analyse_wgs_pindel_prep')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.cgpPindel_annot')

    # block 5
    pipeline.transform(
        task_func=stages.analyse_wgs_cgpFlagCaVEMan,
        name='analyse_wgs_cgpFlagCaVEMan',
        input=[output_from('align'), output_from('analyse_wgs_CaVEMan')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.cgpFlagCaVEMan')

    # pre block 6
    pipeline.transform(
        task_func=stages.analyse_wgs_CaVEMan_annot_prep,
        name='analyse_wgs_CaVEMan_annot_prep',
        input=[output_from('align'), output_from('analyse_wgs_cgpFlagCaVEMan')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.CaVEMan_annot_prep')

    # pre block 6
    pipeline.transform(
        task_func=stages.analyse_wgs_caveman_prep,
        name='analyse_wgs_caveman_prep',
        input=[output_from('align'), output_from('analyse_wgs_CaVEMan_annot_prep')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.caveman_prep')

    # block 6
    pipeline.transform(
        task_func=stages.analyse_wgs_CaVEMan_annot,
        name='analyse_wgs_CaVEMan_annot',
        input=[output_from('align'), output_from('analyse_wgs_caveman_prep')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.CaVEMan_annot')

    # done
    pipeline.transform(
        task_func=stages.analyse_wgs_finish,
        name='analyse_wgs_finish',
        input=[output_from('align'), output_from('analyse_wgs_CaVEMan_annot'), output_from('analyse_wgs_BRASS'), output_from('analyse_wgs_cgpPindel_annot'), output_from('analyse_wgs_alleleCount'), output_from('analyse_wgs_verify_MT'), output_from('analyse_wgs_verify_WT')],
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.wgs.1.1.2/completed.finish')

    #
    # runs the delly singularity container
    #
#    pipeline.transform(
#        task_func=stages.delly,
#        name='delly',
#        input=output_from('align'),
#        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
#        output='{path[0]}/{sample[0]}.delly.completed')

    pipeline.transform(
        task_func=stages.gridss,
        name='gridss',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.gridss.completed')

    pipeline.transform(
        task_func=stages.muse,
        name='muse',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.muse.completed')

    pipeline.transform(
        task_func=stages.mutect1,
        name='mutect1',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.mutect1.completed')

#    pipeline.transform(
#        task_func=stages.mutect2,
#        name='mutect2',
#        input=output_from('align'),
#        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
#        output='{path[0]}/{sample[0]}.mutect2.completed')

    pipeline.transform(
        task_func=stages.platypus,
        name='platypus',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.platypus.completed')

    pipeline.transform(
        task_func=stages.varscan_germline,
        name='varscan_germline',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.varscan.completed')

    pipeline.transform(
        task_func=stages.hmmcopy,
        name='hmmcopy',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.hmmcopy.completed')

    pipeline.transform(
        task_func=stages.callable_bases,
        name='callable_bases',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.callable_bases.completed')

    pipeline.transform(
        task_func=stages.somatic_sniper,
        name='somatic_sniper',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.somatic_sniper.completed')

    pipeline.transform(
        task_func=stages.contest,
        name='contest',
        input=output_from('align'),
        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
        output='{path[0]}/{sample[0]}.contest.completed')

#    pipeline.transform(
#        task_func=stages.delly2,
#        name='delly2',
#        input=output_from('align'),
#        filter=formatter('(?P<path>.+)/(?P<sample>[a-zA-Z0-9]+).mapped.bam'),
#        output='{path[0]}/{sample[0]}.delly2.completed')
    
    return pipeline
