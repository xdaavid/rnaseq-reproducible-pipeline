# Architecture

## Design goals

The workflow is designed around five constraints:

1. A malformed sample sheet must fail before expensive computation starts.
2. Every sample must be processed independently and in parallel.
3. Scientific tools must run in pinned, portable environments.
4. A failed execution must be resumable.
5. Results must include enough provenance to audit how they were produced.

## Module boundaries

| Module | Input | Output | Responsibility |
|---|---|---|---|
| `VALIDATE_SAMPLESHEET` | CSV | normalized CSV | Enforce the input contract |
| `FASTQC` | paired FASTQ | HTML and ZIP | Inspect raw-read quality |
| `FASTP` | paired FASTQ | trimmed FASTQ, JSON, HTML | Adapter and quality trimming |
| `SALMON_INDEX` | transcriptome FASTA | Salmon index | Prepare reference |
| `SALMON_QUANT` | trimmed reads, index | per-sample `quant.sf` | Estimate transcript abundance |
| `MERGE_SALMON` | all quantification directories | count and TPM matrices | Build cohort-level matrices |
| `MULTIQC` | QC and quantification outputs | consolidated HTML report | Summarize run quality |

The workflow orchestration is kept in `main.nf`; executable logic that does not
belong to an external scientific tool lives in `bin/` and is unit tested.

## Dataflow

The validated CSV becomes a channel of tuples:

```text
[
  metadata: [id: "CTRL_01", condition: "control"],
  reads:    ["CTRL_01_R1.fastq.gz", "CTRL_01_R2.fastq.gz"]
]
```

Nextflow broadcasts this channel to FastQC and fastp. The cleaned read channel
feeds Salmon, while the index is a reusable value shared by all samples.
Per-sample directories are collected only when building cohort matrices and
the final MultiQC report.

## Failure model

- Validation and scientific errors terminate the run.
- Exit codes typically associated with infrastructure termination are retried
  once.
- Successful tasks remain in the Nextflow cache and can be reused with
  `-resume`.
- Missing outputs cause the owning process to fail instead of silently
  producing an incomplete result.

## Extension points

Natural additions include:

- `tximport`-based gene aggregation.
- DESeq2 differential expression.
- STAR alignment and BAM quality control.
- Strandedness inference.
- Reference acquisition and checksum validation.
- AWS Batch, Google Batch, Slurm, or Kubernetes execution profiles.
