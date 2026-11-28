# Compares two performance result files captured from `import validate.validate_performance`
# (see validate/validation.md), e.g. the committed results for a board against a new run,
# to spot memory or speed regressions between releases.
#
# Usage (desktop Python):
#   python microcontrollers/compare_results.py <baseline.txt> <new.txt> [--memory 5] [--cycles 10] [--fail]
#
# For every script (and every run within a script, as some run their task more than
# once) this reports:
#   * START used bytes  - heap used before the script did anything.
#   * AFTER GC used     - heap still used after the script finished and a GC ran.
#   * CYCLES K/s        - task cycles per second, where the script reports it.
# A change is flagged as a regression when memory grows by more than --memory percent
# or cycles drop by more than --cycles percent. With --fail the exit code is 1 if any
# regression was found.
import argparse
import re
import sys
from pathlib import Path

SCRIPT_PATTERN = re.compile(r"^/validate/performance/(\S+)\.py output:")
START_PATTERN = re.compile(r"^START \.+ : Used: (\d+) bytes")
AFTER_PATTERN = re.compile(r"^AFTER GC \.+ : Used: (\d+) bytes")
CYCLES_PATTERN = re.compile(r"^CYCLES \.+ : ([\d,.]+) K/s")


def parse(path: Path) -> dict[str, list[dict]]:
    """
    Returns {script: [run, ...]} where each run is a dict with any of the keys
    start, after and cycles.
    """
    results: dict[str, list[dict]] = {}
    runs = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if match := SCRIPT_PATTERN.match(line):
            runs = results.setdefault(match.group(1), [])
            continue
        if runs is None:
            continue
        if match := START_PATTERN.match(line):
            runs.append({"start": int(match.group(1))})
        elif runs and (match := AFTER_PATTERN.match(line)):
            runs[-1]["after"] = int(match.group(1))
        elif runs and (match := CYCLES_PATTERN.match(line)):
            runs[-1]["cycles"] = float(match.group(1).replace(",", ""))
    return results


def percent(old: float, new: float) -> float:
    return 0.0 if old == 0 else (new - old) * 100 / old


def compare(baseline: dict, new: dict, memory_threshold: float, cycles_threshold: float) -> int:
    """
    Prints the comparison table and returns the number of regressions.
    """
    regressions = 0
    print(f"{'script':<32}{'run':>4}{'after GC (bytes)':>26}{'change':>9}{'cycles (K/s)':>22}{'change':>9}")
    for script in sorted(set(baseline) | set(new)):
        old_runs = baseline.get(script, [])
        new_runs = new.get(script, [])
        if not old_runs or not new_runs:
            print(f"{script:<32}  only in {'new' if new_runs else 'baseline'}")
            continue

        for index, (old, cur) in enumerate(zip(old_runs, new_runs)):
            flags = []
            memory = cycles = ""
            memory_change = cycles_change = ""
            if "after" in old and "after" in cur:
                memory = f"{old['after']:>10,} -> {cur['after']:>10,}"
                change = percent(old["after"], cur["after"])
                memory_change = f"{change:+.1f}%"
                if change > memory_threshold:
                    flags.append("MEMORY")
            if "cycles" in old and "cycles" in cur:
                cycles = f"{old['cycles']:>8,.1f} -> {cur['cycles']:>8,.1f}"
                change = percent(old["cycles"], cur["cycles"])
                cycles_change = f"{change:+.1f}%"
                if change < -cycles_threshold:
                    flags.append("CYCLES")

            regressions += len(flags)
            marker = ("  <-- " + ", ".join(flags)) if flags else ""
            print(f"{script:<32}{index + 1:>4}{memory:>26}{memory_change:>9}{cycles:>22}{cycles_change:>9}{marker}")

    print(f"\n{regressions} regression(s) beyond thresholds (memory +{memory_threshold}%, cycles -{cycles_threshold}%)")
    return regressions


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two cptkip performance result files.")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--memory", type=float, default=5.0, help="Flag memory growth above this percent.")
    parser.add_argument("--cycles", type=float, default=10.0, help="Flag cycle drops above this percent.")
    parser.add_argument("--fail", action="store_true", help="Exit with 1 if any regression is found.")
    args = parser.parse_args()

    regressions = compare(parse(args.baseline), parse(args.new), args.memory, args.cycles)
    return 1 if args.fail and regressions else 0


if __name__ == "__main__":
    sys.exit(main())
