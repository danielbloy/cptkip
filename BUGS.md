# cptkip — Bug & Test Gap Analysis

Generated 2026-07-03. Covers all 7 submodules (`core`, `config`, `cpu`, `pin`, `task`,
`device`, `animation`).

## Bugs (highest confidence first)

### Critical

1. **`cptkip/task/resilient_runner.py`** — entire module is an unimplemented stub
   (`# TODO`, no code). It's documented in the README/CLAUDE.md as a first-class task
   runner ("catches errors and restarts failed tasks") but importing/using it does nothing.
2. **`cptkip/animation/flicker.py`** — its test file is fully `@pytest.mark.skip`'d with
   `assert False` as the only line, so `Flicker` has zero real coverage despite being a
   shipped animation.

### Correctness bugs

3. `cptkip/device/melody.py:359-363` — flat→sharp conversion is wrong for **Cb** and
   **Fb**: only "A" is special-cased, so `Cb`→`"B#"` and `Fb`→`"E#"`, neither valid, both
   raise `ValueError("note is invalid")` for legitimate note names.
4. `cptkip/device/melody.py:150-153` — `Melody.tempo = 0` raises an unhandled
   `ZeroDivisionError`; negative tempo silently corrupts timing instead of erroring.
5. `cptkip/device/buzzer.py:39-46` — `beeps(0)` (or negative count) still plays one beep,
   contradicting "plays `count` beeps."
6. `cptkip/device/led.py:47-57` — brightness setter returns early when `|change| < 0.001`
   without ever assigning `self._brightness`, so tiny repeated deltas against a stale
   baseline can never accumulate — a slow fade can get permanently stuck.
7. `cptkip/animation/flicker.py:52-54` — `(base + brightness) & 0xFF` has no clamp; if
   `base + flame > 255` it wraps (e.g. 300→44) instead of clamping to full brightness —
   silent visual corruption.
8. `cptkip/task/periodic_task.py` / `periodic_task_async.py` — `frequency` above 1e9 Hz
   truncates `interval_ns` to 0, causing an infinite loop in the catch-up `while` (hangs
   the thread/event loop). No validation guards against it.
9. `cptkip/pin/buzzer_pin.py` — `frequency` is a plain attribute while `volume` is a
   property that re-applies itself; setting `frequency` directly doesn't update live PWM
   output, an inconsistent, easy-to-misuse API.
10. `cptkip/config/configuration.py:5-20` — `import cptkip.core.logging as logging` can be
    silently shadowed by `from config import *` if the user's `config.py` imports anything
    named `logging` (e.g. stdlib `logging`), causing an `AttributeError` at import time.
11. `cptkip/config/configuration.py:10-18` — `except ImportError` around config loading
    also swallows `ImportError`s raised from inside a real `config.py`, misreporting
    genuine failures as "no config file found."
12. `cptkip/core/environment.py:76` — `__is_running_in_in_ci = True` (typo) creates a dead,
    unused variable instead of confirming the real flag — harmless today but misleading.
13. `cptkip/animation/flicker.py:21-23` — RGB channels stored as `array.array("I", ...)`
    (4-byte ints) for values that are always 0-255; should be `"B"` (1 byte) — 4x memory
    waste, notable given this module is explicitly called out for memory-consciousness.

## Test gaps

- **No tests at all**: `cptkip/core/control.py`, `cptkip/task/resilient_runner.py`
  (matches its stub status), `cptkip/animation/flicker.py` (skipped).
- **Hardware branches never exercised** (because `are_pins_available()` is forced `False`
  in CI): all four `pin/*.py` classes' `digitalio`/`pwmio` code paths, `deinit()`, invert
  logic, and the `pin is None` validation guard; `core/memory.py`'s microcontroller
  `gc.mem_alloc/free` branch; `cpu/cpu.py`'s microcontroller `info()` branch including
  `None`→`"n/a"` substitution; `core/environment.py`'s `BLINKA_U2IF`/`import board` paths.
- **Logging**: `core/logging.py` tests leave `LEVEL=WARNING` throughout, so the
  `DEBUG`/`INFO` prefix branches and actual `print()` call are never hit.
- **Sync/async parity untested**: no test confirms `basic_runner`/`periodic_task` and
  their `_async` counterparts behave equivalently for the same parameters; no test covers
  exceptions raised from `periodic_task`'s `func`/`begin`/`end`/`continue_func` callbacks.
- **Boundary/invalid input untested**: `buzzer_pin`/`pwm_pin` volume clamping outside
  [0,1]; negative frequency in `play()`; `led.py` brightness clamping outside [0,1];
  `button.py` explicitly has a `# TODO: Add tests with pullup = False or pullup with None`;
  melody flat notes ("Cb"/"Fb") and zero/negative tempo (would have caught bugs #3/#4
  above); `buzzer.beeps(0)`/negative (would have caught bug #5).
- `device/pixels.py` desktop mock's no-op methods have no assertions beyond construction.
