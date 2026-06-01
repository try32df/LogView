from pathlib import Path
import tempfile
import unittest

from logview_core import export_text, filter_lines, human_size, tail_lines


class LogViewCoreTests(unittest.TestCase):
    def test_tail_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.log"
            path.write_text("one\ntwo\nthree\nfour\n", encoding="utf-8")
            self.assertEqual(tail_lines(path, 2), ["three\n", "four\n"])

    def test_filter_is_case_insensitive(self):
        lines = ["ERROR disk\n", "Info ok\n", "error network\n"]
        self.assertEqual(filter_lines(lines, "error"), ["ERROR disk\n", "error network\n"])

    def test_human_size(self):
        self.assertEqual(human_size(1024), "1.0 КБ")
        self.assertEqual(human_size(10), "10 Б")

    def test_export(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.txt"
            export_text(path, "hello")
            self.assertEqual(path.read_text(encoding="utf-8"), "hello")

    def test_invalid_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.log"
            path.write_text("line\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                tail_lines(path, 0)


if __name__ == "__main__":
    unittest.main()
