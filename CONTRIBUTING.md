# Contributing

## Development workflow

1. Create a branch from `main`.
2. Keep each pull request focused on one behavior.
3. Add or update tests for every behavior change.
4. Run Python checks and the Nextflow stub integration test.
5. Document scientific assumptions and user-visible parameters.

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m unittest discover -s tests -v
nextflow run main.nf -profile test -stub-run
```

## Module requirements

Every new process should include:

- A semantic `tag`.
- Pinned container and Conda versions.
- Explicit inputs and outputs.
- CPU, memory, and time configuration.
- A `stub` section.
- A version record when it invokes an external tool.

## Scientific changes

Changes that alter biological interpretation must document:

- The scientific question.
- Input assumptions.
- Reference and annotation requirements.
- Expected output.
- Known limitations.
- A reproducible validation dataset.
