process MERGE_SALMON {
    tag 'expression-matrices'

    container 'python:3.12.7-slim'
    conda 'python=3.12.7'

    publishDir "${params.outdir}/matrices", mode: 'copy'

    input:
    path quant_dirs
    path merger

    output:
    path 'transcript_counts.tsv', emit: counts
    path 'transcript_tpm.tsv', emit: tpm

    script:
    def quant_args = quant_dirs.collect { quant_dir -> "\"${quant_dir}\"" }.join(' ')
    """
    python "${merger}" \
        --quant-dirs ${quant_args} \
        --counts transcript_counts.tsv \
        --tpm transcript_tpm.tsv
    """

    stub:
    """
    printf 'transcript\\tSAMPLE_A\\nTX001\\t5.0\\n' > transcript_counts.tsv
    printf 'transcript\\tSAMPLE_A\\nTX001\\t625000.0\\n' > transcript_tpm.tsv
    """
}
