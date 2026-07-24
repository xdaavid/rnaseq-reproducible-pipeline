from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "bin" / "validate_samplesheet.py"
SPEC = importlib.util.spec_from_file_location("validate_samplesheet", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class SamplesheetTests(unittest.TestCase):
    def test_valid_samplesheet_is_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            source = tmp_path / "samples.csv"
            target = tmp_path / "validated.csv"
            source.write_text(
                "sample,condition,fastq_1,fastq_2\n"
                " S1 , control , reads/S1_R1.fastq.gz , reads/S1_R2.fastq.gz \n",
                encoding="utf-8",
            )

            count = MODULE.validate_samplesheet(source, target)

            self.assertEqual(count, 1)
            self.assertEqual(
                target.read_text(encoding="utf-8"),
                "sample,condition,fastq_1,fastq_2\n"
                "S1,control,reads/S1_R1.fastq.gz,reads/S1_R2.fastq.gz\n",
            )

    def test_duplicate_sample_is_rejected(self) -> None:
        rows = [
            {
                "sample": "S1",
                "condition": "control",
                "fastq_1": "S1_R1.fastq",
                "fastq_2": "S1_R2.fastq",
            },
            {
                "sample": "S1",
                "condition": "case",
                "fastq_1": "S2_R1.fastq",
                "fastq_2": "S2_R2.fastq",
            },
        ]

        with self.assertRaisesRegex(
            MODULE.SamplesheetValidationError, "duplicate sample"
        ):
            MODULE.validate_rows(list(MODULE.REQUIRED_COLUMNS), rows)

    def test_missing_column_is_rejected(self) -> None:
        with self.assertRaisesRegex(MODULE.SamplesheetValidationError, "fastq_2"):
            MODULE.validate_rows(["sample", "condition", "fastq_1"], [])

    def test_same_mate_file_is_rejected(self) -> None:
        rows = [
            {
                "sample": "S1",
                "condition": "control",
                "fastq_1": "S1.fastq",
                "fastq_2": "S1.fastq",
            }
        ]

        with self.assertRaisesRegex(MODULE.SamplesheetValidationError, "same file"):
            MODULE.validate_rows(list(MODULE.REQUIRED_COLUMNS), rows)


if __name__ == "__main__":
    unittest.main()
