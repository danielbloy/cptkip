## Bugs

### Critical

1. **`cptkip/animation/flicker.py`** — its test file is fully `@pytest.mark.skip`'d with
   `assert False` as the only line, so `Flicker` has zero real coverage despite being a
   shipped animation.

### Correctness bugs

8. `cptkip/task/periodic_task.py` / `periodic_task_async.py` — `frequency` above 1e9 Hz
   truncates `interval_ns` to 0, causing an infinite loop in the catch-up `while` (hangs
   the thread/event loop). No validation guards against it.
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
