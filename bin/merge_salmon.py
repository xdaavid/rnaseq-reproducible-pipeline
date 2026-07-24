#!/usr/bin/env python3
"""Merge Salmon quant.sf outputs into transcript-level count and TPM matrices."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REQUIRED_QUANT_COLUMNS = {"Name", "TPM", "NumReads"}


class QuantificationError(ValueError):
    """Raised when Salmon output cannot be merged safely."""


def read_quant_file(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Read transcript counts and TPM values from a Salmon quant.sf file."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_QUANT_COLUMNS - columns
        if missing:
            raise QuantificationError(
                f"{path} is missing column(s): {', '.join(sorted(missing))}."
            )

        counts: dict[str, str] = {}
        tpm: dict[str, str] = {}
        for row_number, row in enumerate(reader, start=2):
            transcript = row["Name"].strip()
            if not transcript:
                raise QuantificationError(
                    f"{path}, row {row_number}: transcript name is empty."
                )
            if transcript in counts:
                raise QuantificationError(
                    f"{path}, row {row_number}: duplicate transcript '{transcript}'."
                )
            counts[transcript] = row["NumReads"].strip()
            tpm[transcript] = row["TPM"].strip()

    if not counts:
        raise QuantificationError(f"{path} contains no transcript records.")

    return counts, tpm


def build_matrices(
    quant_dirs: list[Path],
) -> tuple[list[str], list[str], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    """Collect sample quantifications and return matrix components."""
    if not quant_dirs:
        raise QuantificationError("No Salmon quantification directories were supplied.")

    samples: list[str] = []
    counts_by_sample: dict[str, dict[str, str]] = {}
    tpm_by_sample: dict[str, dict[str, str]] = {}
    transcripts: set[str] = set()

    for quant_dir in sorted(quant_dirs, key=lambda path: path.name):
        sample = quant_dir.name
        quant_file = quant_dir / "quant.sf"

        if sample in counts_by_sample:
            raise QuantificationError(f"Duplicate sample directory '{sample}'.")
        if not quant_file.is_file():
            raise QuantificationError(f"Missing Salmon result: {quant_file}.")

        counts, tpm = read_quant_file(quant_file)
        samples.append(sample)
        counts_by_sample[sample] = counts
        tpm_by_sample[sample] = tpm
        transcripts.update(counts)

    return samples, sorted(transcripts), counts_by_sample, tpm_by_sample


def write_matrix(
    output_path: Path,
    samples: list[str],
    transcripts: list[str],
    values_by_sample: dict[str, dict[str, str]],
) -> None:
    """Write a tab-separated transcript-by-sample matrix."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["transcript", *samples])
        for transcript in transcripts:
            writer.writerow(
                [
                    transcript,
                    *[
                        values_by_sample[sample].get(transcript, "0")
                        for sample in samples
                    ],
                ]
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge Salmon quant.sf files into count and TPM matrices."
    )
    parser.add_argument(
        "--quant-dirs",
        required=True,
        nargs="+",
        type=Path,
        help="One or more Salmon output directories.",
    )
    parser.add_argument("--counts", required=True, type=Path)
    parser.add_argument("--tpm", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        samples, transcripts, counts, tpm = build_matrices(args.quant_dirs)
        write_matrix(args.counts, samples, transcripts, counts)
        write_matrix(args.tpm, samples, transcripts, tpm)
    except (OSError, QuantificationError) as exc:
        print(f"Unable to merge Salmon results:\n{exc}", file=sys.stderr)
        return 2

    print(
        f"Merged {len(samples)} sample(s) and {len(transcripts)} transcript(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
