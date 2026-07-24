process SALMON_QUANT {
    tag "${meta.id}"

    container 'quay.io/biocontainers/salmon:1.10.3--h6dccd9a_2'
    conda 'bioconda::salmon=1.10.3'

    publishDir "${params.outdir}/quantification", mode: 'copy'

    input:
    tuple val(meta), path(read1), path(read2)
    path index

    output:
    tuple val(meta), path("${meta.id}"), emit: quant
    path 'versions.yml', emit: versions

    script:
    """
    salmon quant \
        --index "${index}" \
        --libType ${params.salmon_libtype} \
        --mates1 "${read1}" \
        --mates2 "${read2}" \
        --threads ${task.cpus} \
        --validateMappings \
        --gcBias \
        --output ${meta.id}

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        salmon: \$(salmon --version | sed 's/salmon //')
    END_VERSIONS
    """

    stub:
    """
    mkdir -p ${meta.id}/logs
    cat <<-END_QUANT > ${meta.id}/quant.sf
    Name	Length	EffectiveLength	TPM	NumReads
    TX001	120	71	625000.0	5.0
    TX002	140	91	375000.0	3.0
    END_QUANT
    echo '{"percent_mapped": 100.0}' > ${meta.id}/aux_info.json
    echo 'salmon stub' > ${meta.id}/logs/salmon_quant.log
    echo '"SALMON_QUANT": {salmon: "1.10.3"}' > versions.yml
    """
}
