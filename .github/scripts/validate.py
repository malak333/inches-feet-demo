"""Validate the initial scaffold or run nonempty Python application tests."""

from pathlib import Path
import subprocess
import sys
import unittest

SCAFFOLD = {
    "README.md",
    ".github/workflows/ci.yml",
    ".github/scripts/validate.py",
    ".github/scripts/test_validate.py",
}


def main():
    root = Path.cwd()
    tracked = set(subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")) - {""}
    sources = sorted(name for name in tracked if name.endswith(".py") and not name.startswith(".github/"))
    if not sources:
        if tracked != SCAFFOLD or not (root / "README.md").read_text().strip():
            raise SystemExit("Only the exact initial scaffold may pass without application tests.")
        print("Repository scaffold validated; application code has not been published.")
        return

    for name in sources:
        compile((root / name).read_bytes(), name, "exec")
    tests = root / "tests"
    if not tests.is_dir():
        raise SystemExit("Python application code requires tests/ with discoverable unittest tests.")
    sys.path.insert(0, str(root))
    suite = unittest.defaultTestLoader.discover(str(tests))
    if suite.countTestCases() == 0:
        raise SystemExit("No application tests were discovered; refusing an empty green check.")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
