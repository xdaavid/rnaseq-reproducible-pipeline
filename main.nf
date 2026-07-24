nextflow.enable.dsl = 2

include { VALIDATE_SAMPLESHEET } from './modules/local/validate_samplesheet'
include { FASTQC }              from './modules/local/fastqc'
include { FASTP }               from './modules/local/fastp'
include { SALMON_INDEX }        from './modules/local/salmon_index'
include { SALMON_QUANT }        from './modules/local/salmon_quant'
include { MERGE_SALMON }        from './modules/local/merge_salmon'
include { MULTIQC }             from './modules/local/multiqc'

workflow {
    main:
    if (!params.input) {
        error "Missing required parameter: --input"
    }
    if (!params.transcriptome) {
        error "Missing required parameter: --transcriptome"
    }

    def samplesheet_file = file(params.input, checkIfExists: true)
    def transcriptome_file = file(params.transcriptome, checkIfExists: true)

    def samplesheet_ch = channel.value(samplesheet_file)
    def transcriptome_ch = channel.value(transcriptome_file)
    def validator_ch = channel.value(
        file("${projectDir}/bin/validate_samplesheet.py", checkIfExists: true)
    )
    def merger_ch = channel.value(
        file("${projectDir}/bin/merge_salmon.py", checkIfExists: true)
    )

    VALIDATE_SAMPLESHEET(samplesheet_ch, validator_ch)

    def reads_ch = VALIDATE_SAMPLESHEET.out.validated
        .splitCsv(header: true)
        .map { row ->
            def meta = [
                id       : row.sample.toString(),
                condition: row.condition.toString()
            ]
            tuple(
                meta,
                [
                    file(row.fastq_1.toString(), checkIfExists: true),
                    file(row.fastq_2.toString(), checkIfExists: true)
                ]
            )
        }

    FASTQC(reads_ch)
    FASTP(reads_ch)
    SALMON_INDEX(transcriptome_ch)
    SALMON_QUANT(FASTP.out.reads, SALMON_INDEX.out.index)

    def quant_dirs_ch = SALMON_QUANT.out.quant
        .map { _meta, quant_dir -> quant_dir }
        .collect()

    MERGE_SALMON(quant_dirs_ch, merger_ch)

    def fastqc_files_ch = FASTQC.out.reports
        .flatMap { _meta, zip_files, html_files -> zip_files + html_files }

    def fastp_files_ch = FASTP.out.reports
        .flatMap { _meta, json_report, html_report -> [json_report, html_report] }

    def salmon_results_ch = SALMON_QUANT.out.quant
        .map { _meta, quant_dir -> quant_dir }

    def multiqc_inputs_ch = fastqc_files_ch
        .mix(fastp_files_ch, salmon_results_ch)
        .collect()

    MULTIQC(multiqc_inputs_ch)

    onComplete:
    def status = workflow.success ? 'SUCCESS' : 'FAILED'
    log.info """
    RNA-seq reproducible pipeline finished
    --------------------------------------
    Status   : ${status}
    Run name : ${workflow.runName}
    Duration : ${workflow.duration}
    Results  : ${params.outdir}
    """

    onError:
    log.error "Pipeline failed: ${workflow.errorMessage}"
}
