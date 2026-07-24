process SALMON_INDEX {
    tag "${transcriptome.simpleName}"

    container 'quay.io/biocontainers/salmon:1.10.3--h6dccd9a_2'
    conda 'bioconda::salmon=1.10.3'

    publishDir "${params.outdir}/reference", mode: 'copy'

    input:
    path transcriptome

    output:
    path 'salmon_index', emit: index
    path 'versions.yml', emit: versions

    script:
    """
    salmon index \
        --transcripts "${transcriptome}" \
        --index salmon_index \
        --threads ${task.cpus}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        salmon: \$(salmon --version | sed 's/salmon //')
    END_VERSIONS
    """

    stub:
    """
    mkdir -p salmon_index
    touch salmon_index/info.json salmon_index/versionInfo.json
    echo '"SALMON_INDEX": {salmon: "1.10.3"}' > versions.yml
    """
}
