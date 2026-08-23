# Manually run script that compiles the cptkip library to .mpy files using mpy-cross.
#
# Usage:
#   python package.py --mpy-cross <path-to-mpy-cross> [--source cptkip] [--output <dir>]
#
# Every .py file found recursively under the source directory is compiled with
# mpy-cross. The directory structure is mirrored under the output directory, which
# defaults to a "package" directory alongside the source directory, so by default
# cptkip/foo/bar.py compiles to package/cptkip/foo/bar.mpy.
import argparse
import subprocess
import sys
from pathlib import Path


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

    files = sorted(source.rglob("*.py"))
    if not files:
        print(f"No .py files found under {source}")
        return 1

    failures = 0
    for file in files:
        destination = output / file.relative_to(source).with_suffix(".mpy")
        destination.parent.mkdir(parents=True, exist_ok=True)
        print(f"{file.relative_to(source.parent)} -> {destination}")
        result = subprocess.run([args.mpy_cross, str(file), "-o", str(destination)])
        if result.returncode != 0:
            failures += 1

    print(f"Compiled {len(files) - failures} of {len(files)} files.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
