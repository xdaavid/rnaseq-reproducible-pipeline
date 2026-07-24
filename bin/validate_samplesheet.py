#!/usr/bin/env python3
"""Validate and normalize the RNA-seq sample sheet."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REQUIRED_COLUMNS = ("sample", "condition", "fastq_1", "fastq_2")
SAMPLE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
FASTQ_PATTERN = re.compile(r".*\.(fastq|fq)(\.gz)?$", re.IGNORECASE)


class SamplesheetValidationError(ValueError):
    """Raised when a sample sheet does not satisfy the pipeline contract."""


def validate_rows(
    fieldnames: list[str] | None,
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Return normalized rows or raise a single error containing all findings."""
    errors: list[str] = []

    if not fieldnames:
        raise SamplesheetValidationError("The sample sheet is empty or has no header.")

    normalized_headers = [name.strip() for name in fieldnames]
    missing = [
        column for column in REQUIRED_COLUMNS if column not in normalized_headers
    ]
    if missing:
        raise SamplesheetValidationError(
            f"Missing required column(s): {', '.join(missing)}."
        )

    normalized_rows: list[dict[str, str]] = []
    seen_samples: set[str] = set()

    for row_number, row in enumerate(rows, start=2):
        normalized = {
            (key.strip() if key else key): (value.strip() if value else "")
            for key, value in row.items()
        }

        sample = normalized.get("sample", "")
        condition = normalized.get("condition", "")
        fastq_1 = normalized.get("fastq_1", "")
        fastq_2 = normalized.get("fastq_2", "")

        if not sample:
            errors.append(f"Row {row_number}: sample is empty.")
        elif not SAMPLE_PATTERN.fullmatch(sample):
            errors.append(
                f"Row {row_number}: sample '{sample}' contains unsupported characters."
            )
        elif sample in seen_samples:
            errors.append(f"Row {row_number}: duplicate sample '{sample}'.")
        else:
            seen_samples.add(sample)

        if not condition:
            errors.append(f"Row {row_number}: condition is empty.")

        for column, value in (("fastq_1", fastq_1), ("fastq_2", fastq_2)):
            if not value:
                errors.append(f"Row {row_number}: {column} is empty.")
            elif not FASTQ_PATTERN.fullmatch(value):
                errors.append(
                    f"Row {row_number}: {column} must end in .fastq, .fq, "
                    ".fastq.gz, or .fq.gz."
                )

        if fastq_1 and fastq_2 and fastq_1 == fastq_2:
            errors.append(
                f"Row {row_number}: fastq_1 and fastq_2 point to the same file."
            )

        normalized_rows.append(normalized)

    if not rows:
        errors.append("The sample sheet has a header but no sample rows.")

    if errors:
        raise SamplesheetValidationError("\n".join(errors))

    return normalized_rows


def validate_samplesheet(input_path: Path, output_path: Path) -> int:
    """Validate input_path and write a normalized CSV to output_path."""
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = [name.strip() for name in reader.fieldnames or []]

    normalized_rows = validate_rows(fieldnames, rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(normalized_rows)

    return len(normalized_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and normalize a paired-end RNA-seq sample sheet."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input CSV file.")
    parser.add_argument(
        "--output", required=True, type=Path, help="Normalized CSV file."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        count = validate_samplesheet(args.input, args.output)
    except (OSError, SamplesheetValidationError) as exc:
        print(f"Sample sheet validation failed:\n{exc}", file=sys.stderr)
        return 2

    print(f"Validated {count} sample(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
