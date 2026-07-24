process MULTIQC {
    tag 'summary-report'

    container 'quay.io/biocontainers/multiqc:1.25.1--pyhdfd78af_0'
    conda 'bioconda::multiqc=1.25.1'

    publishDir "${params.outdir}/multiqc", mode: 'copy'

    input:
    path inputs

    output:
    path 'multiqc_report.html', emit: report
    path 'multiqc_data', emit: data
    path 'versions.yml', emit: versions

    script:
    """
    multiqc \
        --force \
        --filename multiqc_report.html \
        --title "RNA-seq reproducible pipeline" \
        .

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        multiqc: \$(multiqc --version | sed 's/multiqc, version //')
    END_VERSIONS
    """

    stub:
    """
    mkdir -p multiqc_data
    echo '<html><body>MultiQC stub report</body></html>' > multiqc_report.html
    echo -e 'Sample\\tStatus\\nTEST\\tPASS' > multiqc_data/multiqc_general_stats.txt
    echo '"MULTIQC": {multiqc: "1.25.1"}' > versions.yml
    """
}
