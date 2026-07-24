from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "bin" / "merge_salmon.py"
SPEC = importlib.util.spec_from_file_location("merge_salmon", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def make_quant(directory: Path, rows: list[str]) -> None:
    directory.mkdir()
    (directory / "quant.sf").write_text(
        "Name\tLength\tEffectiveLength\tTPM\tNumReads\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


class MergeSalmonTests(unittest.TestCase):
    def test_build_and_write_matrices(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            sample_a = tmp_path / "SAMPLE_A"
            sample_b = tmp_path / "SAMPLE_B"
            make_quant(
                sample_a,
                ["TX1\t100\t70\t60.0\t6.0", "TX2\t90\t60\t40.0\t4.0"],
            )
            make_quant(
                sample_b,
                ["TX1\t100\t70\t25.0\t2.0", "TX3\t80\t50\t75.0\t8.0"],
            )

            samples, transcripts, counts, tpm = MODULE.build_matrices(
                [sample_b, sample_a]
            )
            counts_path = tmp_path / "counts.tsv"
            tpm_path = tmp_path / "tpm.tsv"
            MODULE.write_matrix(counts_path, samples, transcripts, counts)
            MODULE.write_matrix(tpm_path, samples, transcripts, tpm)

            self.assertEqual(samples, ["SAMPLE_A", "SAMPLE_B"])
            self.assertEqual(transcripts, ["TX1", "TX2", "TX3"])
            self.assertEqual(
                counts_path.read_text(encoding="utf-8"),
                "transcript\tSAMPLE_A\tSAMPLE_B\n"
                "TX1\t6.0\t2.0\n"
                "TX2\t4.0\t0\n"
                "TX3\t0\t8.0\n",
            )
            self.assertIn(
                "TX1\t60.0\t25.0", tpm_path.read_text(encoding="utf-8")
            )

    def test_missing_quant_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            empty_dir = Path(directory) / "EMPTY"
            empty_dir.mkdir()

            with self.assertRaisesRegex(
                MODULE.QuantificationError, "Missing Salmon result"
            ):
                MODULE.build_matrices([empty_dir])


if __name__ == "__main__":
    unittest.main()
