# Scientific decisions

## Why transcript-level quantification?

The MVP uses Salmon because it provides fast transcript abundance estimates
without producing large alignment files. This keeps the workflow practical for
a portfolio project while preserving a realistic RNA-seq processing pattern.

Gene-level aggregation depends on a transcript-to-gene mapping tied to a
specific annotation release. It is deliberately left as a documented
extension rather than hidden behind an arbitrary mapping.

## Why run FastQC before trimming?

Raw-read QC preserves evidence about the original sequencing output. Running
only post-trimming QC can conceal adapter contamination or poor cycle quality
present in the source data.

fastp also emits post-processing metrics, which MultiQC combines with FastQC.

## Why infer library type?

`--salmon_libtype A` makes the test workflow portable across example data.
Production projects should replace it with the known library type or review
Salmon's inference before interpreting results.

## Why no differential expression in version 1?

Differential expression requires biological assumptions that cannot be
validated from FASTQ files alone:

- Adequate biological replication.
- Correct experimental design.
- Batch and confounder information.
- A justified transcript-to-gene mapping.
- Prespecified contrasts.

The pipeline therefore stops at reusable abundance matrices instead of
pretending that a default statistical comparison is universally valid.

## Quality is not a single pass/fail threshold

The workflow exposes metrics but does not discard samples automatically.
Thresholds appropriate for one organism, protocol, or read length may be
inappropriate for another. Automated exclusions should be implemented only
after a project-specific quality plan is defined.
