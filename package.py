# Manually run script that compiles the cptkip library to .mpy files using mpy-cross.
#
# Usage:
#   python package.py --mpy-cross <path-to-mpy-cross> [--source cptkip] [--output <dir>]
#
# Every .py file found recursively under the source directory is compiled with
# mpy-cross; any other file (data files such as .mp3) is copied across verbatim.
# The directory structure is mirrored under the output directory, which defaults
# to a "package" directory alongside the source directory, so by default
# cptkip/foo/bar.py compiles to package/cptkip/foo/bar.mpy.
#
# The top-level __init__.py of the source directory is the exception: it is copied
# (not compiled) so it stays readable, and its __version__ is set to the version in
# pyproject.toml. Only the packaged copy is changed; the source file is left untouched.
import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent / "pyproject.toml"
VERSION_PATTERN = re.compile(r'^__version__\s*=.*$', re.MULTILINE)


def read_version() -> str:
    with PYPROJECT.open("rb") as file:
        return tomllib.load(file)["project"]["version"]


def write_versioned_init(source: Path, destination: Path, version: str) -> bool:
    text = source.read_text()
    text, count = VERSION_PATTERN.subn(f'__version__ = "{version}"', text)
    if count == 0:
        print(f"No __version__ assignment found in {source}")
        return False
    destination.write_text(text)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a directory of .py files to .mpy using mpy-cross.")
    parser.add_argument("--mpy-cross", required=True, help="Path to the mpy-cross executable.")
    parser.add_argument("--source", default="cptkip", help="Directory to compile (default: cptkip).")
    parser.add_argument("--output", default=None,
                        help="Output directory (default: a 'package' directory alongside the source directory).")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.is_dir():
        print(f"Source directory not found: {source}")
        return 1

    output = Path(args.output).resolve() if args.output else source.parent / "package"
    output = output / source.name

    files = sorted(path for path in source.rglob("*") if path.is_file())
    if not files:
        print(f"No files found under {source}")
        return 1

    version = read_version()
    init_file = source / "__init__.py"

    failures = 0
    for file in files:
        destination = output / file.relative_to(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if file == init_file:
            print(f"{file.relative_to(source.parent)} -> {destination} (copied, version {version})")
            if not write_versioned_init(file, destination, version):
                failures += 1
        elif file.suffix == ".py":
            destination = destination.with_suffix(".mpy")
            print(f"{file.relative_to(source.parent)} -> {destination}")
            result = subprocess.run([args.mpy_cross, str(file), "-o", str(destination)])
            if result.returncode != 0:
                failures += 1
        else:
            print(f"{file.relative_to(source.parent)} -> {destination} (copied)")
            shutil.copy2(file, destination)

    print(f"Processed {len(files) - failures} of {len(files)} files.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
