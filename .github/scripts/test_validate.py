"""Exercise the CI entry point in disposable real Git repositories."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[2]
SCAFFOLD = ("README.md", ".github/workflows/ci.yml", ".github/scripts/validate.py",
            ".github/scripts/test_validate.py")


class ValidationTests(unittest.TestCase):
    def check_case(self, files, expected_success):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in SCAFFOLD:
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPOSITORY / name, destination)
            for name, contents in files.items():
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(contents, encoding="utf-8")
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(["git", "add", "--", *SCAFFOLD, *files], cwd=root, check=True)
            result = subprocess.run([sys.executable, ".github/scripts/validate.py"],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode == 0, expected_success,
                             result.stdout + result.stderr)

    def test_initial_scaffold_is_explicitly_supported(self):
        self.check_case({}, True)

    def test_unrecognized_non_python_content_is_not_an_empty_success(self):
        self.check_case({"app.js": "throw new Error('not tested');"}, False)

    def test_application_without_tests_fails(self):
        self.check_case({"app.py": "VALUE = 12\n"}, False)

    def test_empty_test_suite_fails(self):
        self.check_case({"app.py": "VALUE = 12\n", "tests/test_app.py": "# no tests\n"}, False)

    def test_syntax_failure_fails(self):
        self.check_case({"app.py": "def broken(\n"}, False)

    def test_application_tests_run_and_failures_propagate(self):
        test = "import unittest\nimport app\nclass TestApp(unittest.TestCase):\n def test_value(self):\n  self.assertEqual(app.VALUE, 12)\n"
        self.check_case({"app.py": "VALUE = 12\n", "tests/test_app.py": test}, True)
        self.check_case({"app.py": "VALUE = 13\n", "tests/test_app.py": test}, False)


if __name__ == "__main__":
    unittest.main()
