# CLAUDE.md

## Overview

CPTKIP (Circuit Python Toolkit for Interactive Projects) is a Python toolkit providing
reusable building blocks — logging, config, CPU info, async task scheduling, pin
abstraction, hardware device wrappers, and animations — for both CircuitPython
microcontrollers and vanilla desktop Python. It's the spiritual successor to
[pico-interactive](https://github.com/danielbloy/pico-interactive), aiming to be simpler to
use and extend, with a particular focus on reducing memory demands. See `README.md` for
project origins/roadmap and `development_environment.md` for dev environment setup.

## Module structure

`cptkip/` is organized into 7 submodules, listed in dependency order (each depends only on
modules above it, except where noted):

- `core` — execution environment, memory, and logging. No dependencies on other `cptkip`
  modules; required by everything else.
- `config` — overridable configuration properties. Depends on `core`.
- `cpu` — CPU information and operations. Depends on `core`.
- `pin` — abstraction layer for environments with no physical pins. Depends on `core`.
- `task` — async thread runners and task scheduling across CircuitPython and Python.
  Depends on `core`.
- `device` — abstractions for hardware components. Depends on `core` and `pin`.
- `animation` — additional animations such as `Flicker`.

## Repo layout

- `cptkip/` — the library source.
- `examples/` — runnable demo scripts organized into numbered topic folders
  (`1 - Core`, `2 - Tasks`, `3 - Pins`, `4 - Devices`, `5 - Animations`). These double as
  CI integration tests via `examples/test_examples.py`.
- `tests/` — pytest unit tests, mirroring `cptkip/` structure
  (`tests/cptkip/<module>/test_*.py`), with shared helpers in `tests/cptkip/utilities.py`.
- `validate/` — manual, on-device validation scripts (`validate_all.py` runs them all);
  not part of the standard CI test run.
- `CircuitPython/` — vendored firmware (`.uf2`) and compiled libs (`.mpy`) per
  CircuitPython version. Large binary assets — do not edit.
- `config.py` (repo root) — shared config used by `examples/` and `validate/`.

## Build / test / lint commands

Pulled directly from `.github/workflows/python-app.yml` — use these verbatim:

- Install: `pip install -r requirements.txt && pip install -e .`
- Unit tests: `pytest tests/`
- Example tests: `PYTHONPATH=../.. pytest examples/` (the `PYTHONPATH` is required so
  `config.py` at the repo root is importable — easy to forget)
- Lint (hard gate): `flake8 cptkip --count --select=E9,F63,F7,F82 --show-source --statistics`
- Lint (informational only, exit-zero): complexity/style pass with
  `--max-complexity=10 --max-line-length=127`
- Validate (on-device style, not run in CI as a test gate): `PYTHONPATH=. python validate/validate_all.py`
- Target Python: 3.12–3.14 (CI matrix runs all three)

## Conventions

- No black/ruff/isort configured. Formatting is handled by **PyCharm's "Reformat on Save"**
  (enabled via Settings → Tools → Actions on Save), using PyCharm's built-in code formatter
  rather than a standalone tool — there's no config file for it in the repo. Claude cannot
  trigger this automatically, so match the formatting already present in surrounding code
  (PyCharm defaults: 4-space indent, double-quoted strings, blank-line and import-ordering
  conventions per PEP 8) and stay within flake8's 127-char line length and complexity ≤10
  guidance.
- **Memory-consciousness**: this library targets memory-constrained microcontrollers
  (Pico-class boards). This is a stated project goal (see README "Origins"), not just a
  style preference — prefer lightweight patterns and avoid gratuitous allocations or heavy
  abstractions, especially in `core`, `device`, and `animation`.
- Unit tests mirror source layout 1:1; put new tests under the matching
  `tests/cptkip/<module>/` path.

## License

Licensed under CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike) — unusual for a code
project. Noncommercial use only, share-alike required. Keep this in mind before suggesting
commercially-oriented features or third-party integrations with incompatible terms.

## Do not touch

- `CircuitPython/` — vendored firmware/`.mpy` binaries.
- `.idea/` — PyCharm project config.

## Branches

CI runs on push to any branch and on PRs targeting `main` or `develop`. Default to
branching from and targeting `main` unless told otherwise for a specific task.
