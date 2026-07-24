# Results and interpretation

## MultiQC

Open `results/multiqc/multiqc_report.html` first. It provides a cohort-wide
view of raw-read quality, trimming, and Salmon quantification.

Review at minimum:

- Per-base quality.
- Adapter content.
- Read counts before and after trimming.
- Percentage of reads retained.
- Sequence duplication.
- GC distribution.
- Salmon mapping rate.

Warnings are not automatically failures. They should be interpreted in the
context of library preparation, organism, read length, and experimental
design.

## Transcript counts

`transcript_counts.tsv` contains Salmon estimated read counts:

```text
transcript    CTRL_01    CTRL_02    CASE_01    CASE_02
TX001            35.2       40.1      120.8      118.3
```

Salmon counts are estimates and may be fractional. Do not round them before a
method explicitly requires integer counts.

## TPM

`transcript_tpm.tsv` contains transcripts per million. TPM is useful for
within-sample abundance summaries and visualization. Raw TPM should not be
used as the direct input to DESeq2.

## Quantification directories

Every sample directory preserves Salmon's original `quant.sf`, logs, and
auxiliary information. These files are the authoritative inputs to downstream
aggregation.

## Execution provenance

`pipeline_info/` records:

- Task commands and status.
- CPU and memory allocation.
- Runtime and peak resources.
- Workflow dependency graph.
- Normalized sample sheet.

Keep this directory with every published result.
