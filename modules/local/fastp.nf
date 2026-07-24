process FASTP {
    tag "${meta.id}"

    container 'quay.io/biocontainers/fastp:0.24.0--heae3180_1'
    conda 'bioconda::fastp=0.24.0'

    publishDir "${params.outdir}/trimmed", mode: 'copy',
        pattern: '*.trimmed.fastq.gz',
        enabled: params.save_trimmed.toString().toBoolean()
    publishDir "${params.outdir}/qc/fastp", mode: 'copy',
        pattern: '*.{json,html}'

    input:
    tuple val(meta), path(reads)

    output:
    tuple val(meta),
        path("${meta.id}_R1.trimmed.fastq.gz"),
        path("${meta.id}_R2.trimmed.fastq.gz"),
        emit: reads
    tuple val(meta),
        path("${meta.id}.fastp.json"),
        path("${meta.id}.fastp.html"),
        emit: reports
    path 'versions.yml', emit: versions

    script:
    """
    fastp \
        --in1 "${reads[0]}" \
        --in2 "${reads[1]}" \
        --out1 ${meta.id}_R1.trimmed.fastq.gz \
        --out2 ${meta.id}_R2.trimmed.fastq.gz \
        --thread ${task.cpus} \
        --qualified_quality_phred ${params.min_quality} \
        --length_required ${params.min_length} \
        --detect_adapter_for_pe \
        --json ${meta.id}.fastp.json \
        --html ${meta.id}.fastp.html

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        fastp: \$(fastp --version 2>&1 | sed 's/fastp //')
    END_VERSIONS
    """

    stub:
    """
    touch ${meta.id}_R1.trimmed.fastq.gz
    touch ${meta.id}_R2.trimmed.fastq.gz
    echo '{}' > ${meta.id}.fastp.json
    echo '<html><body>fastp stub</body></html>' > ${meta.id}.fastp.html
    echo '"FASTP": {fastp: "0.24.0"}' > versions.yml
    """
}
