# Reproducible RNA-seq Pipeline

A GitHub-ready, containerized Nextflow DSL2 workflow that converts paired-end
RNA-seq reads into transcript-level abundance matrices and quality-control
reports.

The project demonstrates the engineering practices expected in modern
bioinformatics roles: input validation, modular workflows, pinned
dependencies, containers, automated tests, CI, provenance, and resumable
execution.

## What the pipeline does

```text
samplesheet.csv
      |
      v
Validate sample metadata
      |
      +--------------------+
      |                    |
      v                    v
FastQC                fastp trimming
                           |
transcriptome.fa           v
      |               trimmed FASTQ
      v                    |
Salmon index               v
      +--------------> Salmon quant
                               |
                     +---------+---------+
                     |                   |
                     v                   v
              count/TPM matrices      MultiQC report
```

### Workflow steps

1. Validate sample names, conditions, mate pairs, and file extensions.
2. Run FastQC on the raw paired-end reads.
3. Trim adapters and low-quality sequence with fastp.
4. Build a versioned Salmon transcriptome index.
5. Quantify transcript abundance independently for every sample.
6. Merge `quant.sf` files into count and TPM matrices.
7. Aggregate quality metrics with MultiQC.
8. Record execution trace, resource usage, timeline, and workflow graph.

## Requirements

- Nextflow `26.04.2` or newer.
- Java 17 or newer.
- Docker, recommended for real analysis.
- Linux, macOS, or Windows through WSL2.

No local installation of FastQC, fastp, Salmon, or MultiQC is required when
using the Docker profile.

Windows users should follow [`docs/WINDOWS_WSL.md`](docs/WINDOWS_WSL.md).
Nextflow must be run inside WSL2 rather than directly from PowerShell.

## Quick verification

The test profile includes a small synthetic dataset. Stub mode checks the
complete workflow graph without downloading bioinformatics containers:

```bash
nextflow run main.nf -profile test -stub-run
```

This is the same lightweight workflow test executed by GitHub Actions.

## Run a real analysis

Create a sample sheet:

```csv
sample,condition,fastq_1,fastq_2
CTRL_01,control,/data/CTRL_01_R1.fastq.gz,/data/CTRL_01_R2.fastq.gz
CTRL_02,control,/data/CTRL_02_R1.fastq.gz,/data/CTRL_02_R2.fastq.gz
CASE_01,disease,/data/CASE_01_R1.fastq.gz,/data/CASE_01_R2.fastq.gz
CASE_02,disease,/data/CASE_02_R1.fastq.gz,/data/CASE_02_R2.fastq.gz
```

Run the workflow:

```bash
nextflow run main.nf \
  -profile docker \
  --input samplesheet.csv \
  --transcriptome references/transcripts.fa \
  --outdir results
```

Resume after an interruption without repeating successful tasks:

```bash
nextflow run main.nf \
  -profile docker \
  --input samplesheet.csv \
  --transcriptome references/transcripts.fa \
  --outdir results \
  -resume
```

Relative FASTQ paths are interpreted from the directory where Nextflow is
launched. Absolute paths are recommended for production runs.

## Main parameters

| Parameter | Description | Default |
|---|---|---:|
| `--input` | Paired-end sample sheet in CSV format | required |
| `--transcriptome` | Transcriptome reference in FASTA format | required |
| `--outdir` | Output directory | `results` |
| `--min_length` | Minimum read length retained by fastp | `30` |
| `--min_quality` | Minimum qualified Phred score | `20` |
| `--salmon_libtype` | Salmon library type; `A` enables inference | `A` |
| `--save_trimmed` | Publish trimmed FASTQ files | `false` |

The complete machine-readable parameter definition is in
[`nextflow_schema.json`](nextflow_schema.json).

## Results

```text
results/
├── matrices/
│   ├── transcript_counts.tsv
│   └── transcript_tpm.tsv
├── multiqc/
│   ├── multiqc_report.html
│   └── multiqc_data/
├── pipeline_info/
│   ├── execution_report.html
│   ├── execution_timeline.html
│   ├── execution_trace.txt
│   ├── samplesheet.valid.csv
│   └── workflow_dag.html
├── qc/
│   ├── fastp/
│   └── fastqc/
├── quantification/
│   ├── CASE_01/
│   └── CTRL_01/
├── reference/
│   └── salmon_index/
└── trimmed/                 # only when --save_trimmed true
```

See [`docs/RESULTS.md`](docs/RESULTS.md) for interpretation guidance.

## Reproducibility features

- Each scientific tool is pinned to a specific container and Conda version.
- Independent samples execute in parallel.
- `-resume` reuses cached successful tasks.
- Every process has explicit CPU, memory, and time requirements.
- Input validation fails early with actionable errors.
- Python utilities have unit tests and no runtime dependencies.
- Stub commands test workflow wiring without large downloads.
- GitHub Actions checks Python code and the complete workflow graph.
- Nextflow produces execution, timeline, trace, and DAG reports.

## Development

Run the Python checks:

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m unittest discover -s tests -v
nextflow lint .
```

Run the workflow integration test:

```bash
nextflow run main.nf -profile test -stub-run
```

Contribution guidance is in [`CONTRIBUTING.md`](CONTRIBUTING.md).
The checks performed on this release are recorded in
[`docs/VALIDATION.md`](docs/VALIDATION.md).

## Scientific scope and limitations

- This workflow performs transcript-level quantification, not gene-level
  differential expression.
- Salmon library-type inference should be reviewed for every experimental
  protocol.
- The supplied test data are synthetic and intended only for software tests.
- Reference provenance is the user's responsibility; production analyses
  should document transcriptome source, organism, assembly, and release.
- A successful workflow does not by itself guarantee that an experiment has
  sufficient replication or a valid biological design.
- This software is for research and education, not clinical diagnosis.

The reasoning behind these boundaries is documented in
[`docs/SCIENTIFIC_DECISIONS.md`](docs/SCIENTIFIC_DECISIONS.md).

## Portfolio value

This repository is intentionally designed to show more than a one-off
analysis. It demonstrates:

- Linux-oriented workflow automation.
- Nextflow DSL2 and dataflow programming.
- Docker and dependency pinning.
- RNA-seq quality control and transcript quantification.
- Python validation and data transformation.
- Testing, CI, failure handling, and documentation.

Suggested résumé wording and interview topics are available in
[`docs/PORTFOLIO.md`](docs/PORTFOLIO.md).

## References

- [Nextflow documentation](https://www.nextflow.io/docs/latest/)
- [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [fastp](https://github.com/OpenGene/fastp)
- [Salmon](https://combine-lab.github.io/salmon/)
- [MultiQC](https://docs.seqera.io/multiqc/)

## License

MIT. See [`LICENSE`](LICENSE).
