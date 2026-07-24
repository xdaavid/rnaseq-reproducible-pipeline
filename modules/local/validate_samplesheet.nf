process VALIDATE_SAMPLESHEET {
    tag 'samplesheet'

    container 'python:3.12.7-slim'
    conda 'python=3.12.7'

    publishDir "${params.outdir}/pipeline_info", mode: 'copy'

    input:
    path samplesheet
    path validator

    output:
    path 'samplesheet.valid.csv', emit: validated

    script:
    """
    python "${validator}" \
        --input "${samplesheet}" \
        --output samplesheet.valid.csv
    """

    stub:
    """
    cp "${samplesheet}" samplesheet.valid.csv
    """
}
