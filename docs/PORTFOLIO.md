# Presenting this project in a portfolio

## One-line description

Built a containerized Nextflow RNA-seq workflow that validates paired-end
samples, performs QC and trimming, quantifies transcripts with Salmon, and
produces cohort matrices plus auditable execution reports.

## Suggested résumé bullets

- Developed a modular RNA-seq pipeline in Nextflow DSL2 with Docker-pinned
  FastQC, fastp, Salmon, and MultiQC processes.
- Implemented early sample-sheet validation, parallel per-sample processing,
  resumable execution, provenance reports, and tested Python utilities.
- Added GitHub Actions integration tests using Nextflow stub execution,
  enabling rapid validation without downloading reference datasets or
  containers.

## Interview topics

Be prepared to explain:

1. Why workflow managers are preferable to a long Bash script.
2. How channels allow per-sample parallelism.
3. What Docker contributes to reproducibility and what it does not guarantee.
4. Why FastQC warnings require biological context.
5. Why TPM is not a direct replacement for count-based statistical models.
6. How `-resume` works and when a cached task is invalidated.
7. Why sample validation should occur before expensive tools start.
8. How you would scale the workflow to Slurm or cloud batch execution.

## Useful demo sequence

1. Show the sample sheet contract.
2. Run the stub profile in under a minute.
3. Open the workflow DAG.
4. Show one process module and its pinned container.
5. Trigger a duplicate-sample validation error.
6. Show unit tests and the CI workflow.
7. Explain the boundary between quantification and differential expression.

## Strong extensions

Choose one rather than adding many unfinished features:

- Gene-level aggregation and DESeq2 with a validated design file.
- A cloud execution profile and cost report.
- nf-test process-level tests.
- Reference download with checksums and annotation provenance.
- A small web interface that generates validated sample sheets.
