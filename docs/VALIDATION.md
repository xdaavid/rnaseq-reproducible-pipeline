# Validation record

This document records the checks performed before the repository was
packaged. GitHub Actions repeats the automated checks on every push and pull
request.

## Passed checks

- Nextflow 26.04.4 strict-syntax lint across `main.nf` and all local modules.
- Six Python unit tests for sample-sheet validation and Salmon matrix merging.
- Ruff 0.8.4 static analysis.
- Python bytecode compilation.
- Validation of all synthetic FASTQ records, including equal sequence and
  quality lengths.
- JSON parsing of `nextflow_schema.json`.
- Comparison of generated count and TPM matrices against expected fixtures.

## Integration execution

The CI workflow runs the complete workflow graph on Ubuntu:

```bash
nextflow run main.nf -profile test -stub-run
```

The release workstation was native Windows without WSL2. Nextflow correctly
refused native execution because it requires a POSIX-compatible environment.
The workflow therefore received local strict-syntax validation, while the
portable stub integration run is delegated to the included Ubuntu GitHub
Actions job.

## What the stub test does not prove

Stub mode validates channel wiring, process scheduling, declared outputs, and
report generation without executing the real bioinformatics tools. Before
using the workflow for research, run the Docker or Conda profile with a small
representative dataset and inspect FastQC, fastp, Salmon, and MultiQC outputs.
