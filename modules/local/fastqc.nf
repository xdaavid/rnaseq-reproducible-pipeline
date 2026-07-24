process FASTQC {
    tag "${meta.id}"

    container 'quay.io/biocontainers/fastqc:0.12.1--hdfd78af_0'
    conda 'bioconda::fastqc=0.12.1'

    publishDir "${params.outdir}/qc/fastqc", mode: 'copy'

    input:
    tuple val(meta), path(reads)

    output:
    tuple val(meta), path('*_fastqc.zip'), path('*_fastqc.html'), emit: reports
    path 'versions.yml', emit: versions

    script:
    def read_args = reads.collect { read -> "\"${read}\"" }.join(' ')
    """
    fastqc \
        --threads ${task.cpus} \
        --quiet \
        ${read_args}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        fastqc: \$(fastqc --version | sed 's/FastQC v//')
    END_VERSIONS
    """

    stub:
    def prefixes = reads.collect { read ->
        read.name.replaceFirst(/\.f(ast)?q(\.gz)?$/, '')
    }
    def zip_outputs = prefixes.collect { prefix -> "${prefix}_fastqc.zip" }.join(' ')
    def html_outputs = prefixes.collect { prefix -> "${prefix}_fastqc.html" }.join(' ')
    """
    touch ${zip_outputs}
    touch ${html_outputs}
    echo '"FASTQC": {fastqc: "0.12.1"}' > versions.yml
    """
}
