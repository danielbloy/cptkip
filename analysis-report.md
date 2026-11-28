# CPTKIP Project Analysis Report

*Date: 2026-11-28 · Baseline: `main` @ `e8179aa` ("Prepare for 0.3.6")*

## How this analysis was done

- Read all of `cptkip/` (core, config, cpu, pin, task, device, animation, network, zero), `validate/`
  (drivers, per-module scripts, the performance harness), packaging/CI files, and a sample of
  `examples/` and `tests/`.
- Ran the unit tests (`pytest tests/`: **331 passed**, ~113 s on Python 3.13.1) with line coverage
  (**88 % overall**).
- **Tracking:** fix progress for every item is in [§8 Fix tracking](#8-fix-tracking). Each fix PR
  updates its own entries there.
- **Double-checking:** each defect marked ✅ below was reproduced by running a script against the
  current code (desktop Python) or by building the package. Items marked 🔍 were confirmed by reading
  the code, usually because they only occur when `are_pins_available()` is true or on CircuitPython,
  which can't run on a desktop. Items marked ⚠️ are high-confidence but should be checked on a
  device before acting.
- flake8 is not installed locally, so the lint gate was **not** re-run.

Severity: **High** = wrong behaviour users will hit, or broken packaging/CI. **Medium** = wrong
behaviour in less common paths, or a resource leak. **Low** = edge case, cosmetic, or docs.

---

## 1. Possible defects

### High

| # | Location | Defect | Check |
|---|----------|--------|-------|
| D1 | `pyproject.toml:24` | `packages = ["cptkip"]` lists only the top-level package. A non-editable `pip install .` / wheel contains **only `cptkip/__init__.py`**: no subpackages and no `mp3.mp3`. CI hides this because it uses `pip install -e .`. | ✅ built a wheel: contents = `['cptkip/__init__.py']` |
| D2 | `pyproject.toml:17` | Classifier `"Development Status :: 5 - Stable"` is not a valid trove classifier (the valid one is `5 - Production/Stable`). PyPI rejects uploads that use it. | 🔍 |
| D3 | `device/melody.py:172-186` (`reset`) + `MelodySequence.activate` | If `reset()` is called while paused, it sets `_index = 1` and `_time_left_at_pause = 0`. `resume()` then plays note 0 with no time left, so the next `update()` jumps straight to note 1. **The first note is effectively skipped.** This happens on every loop of a `MelodySequence` and on `previous()`/`activate()`, because finished melodies are paused. | ✅ 0.1 s first note was replaced by note 2 within 50 ms |
| D4 | `device/buzzer.py:44-48` + `pin/buzzer_pin.py:51-59` | Setting `Buzzer.volume` after any tone has played **turns the buzzer back on** (`BuzzerPin.volume` calls `play(self.frequency)`), but `Buzzer._playing` stays `False`, so `update()` never turns it off. The tone sounds until something else stops it. | ✅ `buzzer.playing False`, `pin.playing True` |
| D5 | `zero/button.py:15`, `zero/led.py:14` | The `x or config.X` pattern ignores falsy overrides. `create_button_pin(pullup=False)` and `create_led_pin(invert=False)` silently use the config value instead. Also, `pullup=None` means "external resistor" in `InputPin` but "use config" here, so the zero API can't ask for an external pull. | ✅ both returned `True` |
| ~~D6~~ | `validate/core/cpu.py:4-6`, `examples/2 - Tasks/{e,f}_*.py` | **Withdrawn.** I flagged nested-quote f-strings as SyntaxErrors on CircuitPython. The maintainer has confirmed through on-device testing that they work. | ❌ withdrawn |
| D7 | `pin/input_pin.py:44-48`, `output_pin.py:39-43`, `pwm_pin.py:40-44` | `deinit()` calls `self._pin.deinit()` / `self._pwm.deinit()` without checking for `None`. A **second `deinit()` raises `AttributeError`** when pins are available, e.g. a context manager exit after an explicit `deinit()`, or `Led.deinit()` after the pin was released. `Audio`/`BuzzerPin` say double deinit is safe. These pin classes don't, and the desktop tests that "call deinit multiple times" never reach this branch. | 🔍 |

### Medium

| # | Location | Defect | Check |
|---|----------|--------|-------|
| D8 | `device/audio.py:27,57` | `play()` opens a new file each time and never closes the previous one, and `deinit()` doesn't close it either. File handles stay open until GC, which matters on CircuitPython's small FS-handle budget. | 🔍 |
| D9 | `device/audio.py:27` | The placeholder decoder file is opened as `"cptkip/mp3.mp3"`, relative to the CWD. It only works if `cptkip/` is at the drive root. It breaks if the library is in `/lib` (the CircuitPython convention) or if a desktop/Blinka program runs from another directory. | 🔍 |
| D10 | `device/audio.py:3-8,27` | If `from audiomp3 import MP3Decoder` fails, the `ImportError` is swallowed, and `Audio()` later raises a confusing `NameError` instead of a clear "MP3 not supported" error. | 🔍 |
| D11 | `network/biplane.py:129` | `Response(..., headers={})` uses a mutable default. Every `Response` built without explicit headers **shares one dict**, so a header added to one response appears on all later ones. | ✅ `a.headers is b.headers → True` |
| D12 | `network/biplane.py:315,324` | The default `listen_on=(get_host(), get_port())` is evaluated **once, at import time**. On desktop, importing the module opens a UDP socket to probe the IP. Under test, both methods also get frozen (and different) random ports. | 🔍 |
| D13 | `network/biplane.py:191-192` | (Upstream bug) "excessively long or invalid start line, giving up" is printed, but the function doesn't `return`, so processing continues with a truncated line. | 🔍 |
| D14 | `task/*` runners + tasks with `end` | When a runner is given a `continue_func`, `basic_runner`/`reliable_runner` return **before** the tasks see `continue_func() == False`, and the async runners cancel tasks instead. So **task `end` callbacks never run on runner-driven shutdown**. This contradicts the 0.3.3 changelog ("`end` is called now if there is an early exit"), and `validate/utils.execute` relies on exactly this pattern. | 🔍 |
| D15 | `core/logging.py:28-36` | `stacktrace()` formats the whole traceback (several string allocations) **before** checking the log level, even though it only logs at DEBUG. `reliable_runner` calls it on every exception, which is wasteful on-device and risky when memory is low. | 🔍 |
| D16 | `task/limiters.py:22-37` | `duration_limiter` uses `time.time()`, which is wall-clock (subject to NTP jumps) and **integer seconds on CircuitPython**, so `duration_limiter(0.5)` is coarse on-device. Use `monotonic`. | 🔍 |
| D17 | `task/triggered_task*.py`, `triggered_events_task*.py`, `biplane.py` | `time.monotonic()` returns a float, and CircuitPython floats are 30-bit, so resolution degrades as uptime grows (documented CircuitPython caveat). Long-running installations will see increasingly sloppy trigger durations and event timings. | ⚠️ |
| D18 | `task/periodic_task*.py:39-43` | The interval is computed in floating point (`1 / frequency * NS_PER_SECOND`). With CircuitPython's float32 a 3 Hz period becomes 333 333 344 ns instead of 333 333 333, a small cumulative drift. `memory_monitor_task` already uses exact `NS_PER_SECOND // frequency`. | ✅ simulated float32 |
| D19 | `device/melody.py:132-155` | When a non-looping melody finishes, `resume()` briefly plays the *last* note (index −1) before restarting at note 0. | 🔍 |

### Low

| # | Location | Defect |
|---|----------|--------|
| D20 | `core/memory.py:66-68` | Desktop report ends with a stray `"Total:"` (✅ output: `… Free: 13207 MB, Total:`). |
| D21 | `device/melody.py:370-406` | `Cb`, `Fb`, `E#`, `B#` raise `ValueError` (✅). Flats are converted by subtracting a letter, which gives `B#`/`E#`, and those aren't in the table. |
| D22 | `device/melody.py:351-353` | A note with no `:` raises `IndexError`, not `ValueError` (✅). The docstring says the separator is a comma. Octaves are limited to a single digit. |
| D23 | `task/triggered_events_task*.py:74-80` | An empty event tuple `()` raises `IndexError`, not the documented `ValueError` (✅). |
| D24 | `task/periodic_task*.py` | `frequency > 1e9` gives `interval_ns == 0`, so the catch-up `while` loop never terminates. Also, after a long stall that loop runs once per missed period; it could use arithmetic instead. |
| D25 | `device/led.py:185` | `Led[i]` returns floats (`(127.5, 127.5, 127.5)`, ✅) where animation code expects ints. `_parse_color` doesn't mask ints above `0xFFFFFF`. |
| D26 | `device/audio.py:45` | `Audio.deinit()` sets `self.pin = None`, but `Audio` has no `pin` attribute. |
| D27 | `task/triggered_events_task.py:97-101` | If the sync handler is called again after returning `False`, it calls `end()` again because `running` is never cleared. |
| D28 | `zero/pixels.py:32` | `stop_pixels()` sets `brightness = 0.0` permanently, so any later animation on the same strand is invisible unless brightness is restored. Confirm this is intended. |
| D29 | `pin/buzzer_pin.py:102` | Duty cycle is `volume * 2**10`, a maximum of about 1.6 % of 65535. Piezo loudness peaks near 50 %. Confirm this mapping is intended; it makes `volume=1.0` fairly quiet. |

---

## 2. Performance optimisation (memory first, then CPU)

| # | Area | Opportunity | Expected gain |
|---|------|-------------|---------------|
| P1 | All timing (`periodic_task`, `memory_monitor`, `Buzzer`, `Melody`) | `time.monotonic_ns()` exceeds CircuitPython's small-int range (about ±2³⁰) after about 1 s of uptime, so **every call and every add/compare allocates a long int on the heap**. Switch the hot paths to `supervisor.ticks_ms()` with wrap-safe diff (the `adafruit_ticks` pattern), keeping `monotonic_ns` on desktop. This also fixes D17. | Removes per-loop heap churn from every task, which is the biggest single GC-pressure source |
| P2 | `pin/buzzer_pin.py:95-99` + `Melody.update` | `BuzzerPin.off()` *is* `deinit()`, and `Melody.update()` calls `off()` before every note, so **every note deinitialises and reallocates a `PWMOut`**. Create it once with `variable_frequency=True`, change `.frequency`, and silence with `duty_cycle = 0`. Caveat: on RP2040, variable-frequency PWM claims the whole slice. | Removes an object allocation and a pin claim/release per note; smoother audio |
| P3 | `task/triggered_events_task*.py:106,124,142` | Each trigger copies `events` (`events.copy()`), and each tick while running builds `events_to_fire` and runs O(n²) `remove()`s. Sort the events once in `create()` and walk them with an integer index: no per-tick allocations. | Removes per-tick list allocations |
| P4 | `task/periodic_task_async.py`, `triggered_*_async.py`, `memory_monitor_task_async.py` | They loop with `await sleep(1 µs)`, which is effectively a busy-wait (100 % CPU on desktop, no idle on-device). Sleep until the next due time, or `period / PERIODIC_LOOP_WAIT_RATIO`. That constant exists in `core/control.py` but **is not used anywhere** except a test. | Large CPU/power saving for async users |
| P5 | `core/logging.py:stacktrace` | Return early if `LEVEL < DEBUG` before importing `traceback` and formatting (see D15). | Avoids allocations on every caught exception |
| P6 | `config/configuration.py` & `core/__init__.py` | Importing them prints about 8 lines, and the string constants stay resident. Gate these behind a `VERBOSE`/log-level check, or move them into a `report()` function like `environment.report`. | Small RAM saving; quieter output |
| P7 | `animation/flicker.py:58-64` | `draw()` does three float multiply/divides per pixel and recomputes `base + brightness`. Use integer maths (`(c * level) >> 8`, or `// 255`). RP2040 has no FPU, so this is software float. | Faster animation frame |
| P8 | `cpu/cpu.py:16-20` | Each property is read twice (once for the `None` check, once for the value), which means two hardware reads. Read each one once. (`validate/core/cpu.py` also calls `cpu.info()` 8 times.) | Minor |
| P9 | `device/led.py:170-176` | `__setitem__` parses the colour, then `fill()` parses it again. | Minor |
| P10 | `task/triggered_*` (×4) | The identical `Trigger` class is defined four times, so importing sync and async variants creates duplicate class objects. Move it to one module (for example `task/trigger.py`). | Small RAM + maintenance |
| P11 | `zero/led.py`, `zero/pixels.py` | Both import `adafruit_led_animation` (`Animation`, `AnimationSequence`) at module load just for `isinstance`/type hints, even when you only want `create_led()`. Import lazily inside `stop_animation`. | Avoids loading the animation library when it isn't needed |

---

## 3. Missing tests / test gaps

Coverage by module (lines): task 100 %, zero 99 %, device 91 % (audio 69 %), pin 85 % (input 69 %),
core 87 % (environment 73 %), config 82 %, network 60 % (requests 22 %, biplane 63 %).

**Regression tests for the defects above** (none of these are tested today):

- T1 – Melody first-note duration after `reset()` while paused, and across a `MelodySequence` loop (D3, D19).
- T2 – `Buzzer.volume` set while idle must not start sound (D4).
- T3 – `zero.create_*` with `False`/`0` overrides (D5).
- T4 – Double `deinit()` on `InputPin`/`OutputPin`/`PwmPin` **with pins available** (D7). This needs
  fake `digitalio`/`pwmio` modules injected through `monkeypatch.setitem(sys.modules, …)` and
  `environment.are_pins_available` patched to `True`. The same fakes would let you test the hardware
  branches in pin/audio/pixels, which are currently 0 %.
- T5 – `Response` header isolation (D11); `standardise_note` for `Cb/Fb/E#/B#` (D21); malformed
  `decode_melody` input and empty event tuples (D22, D23).
- T6 – `end` callbacks when a runner's `continue_func` stops execution (D14). Decide the intended
  behaviour first.

**Structural gaps:**

- T7 – **Packaging:** nothing builds and imports the wheel (D1/D2). Add a CI step: `pip wheel . &&`
  install into a fresh venv `&& python -c "import cptkip.task.basic_runner"`.
- ~~T8~~ – **Withdrawn** together with D6. On-device testing has already confirmed the f-string syntax works.
- T9 – `network/biplane.py` error paths: 413, malformed start line/headers, too many headers,
  request timeout, 404 vs method mismatch.
- T10 – `core/environment.py` branches: `BLINKA_U2IF`, CI-forcing, `report()` CI line. Use
  `importlib.reload` with `monkeypatch.setenv` (in-process, matching existing test style).
- T11 – `config/configuration.py`: `device.py` overriding `config.py`, and LOG_LEVEL applied after both.
- T12 – Sync/async parity (already listed in `roadmap.md`) and exceptions raised from `periodic_task`
  `begin`/`end`/`continue_func`.
- T13 – Lint scope: CI runs flake8 on `cptkip/` only. Adding `examples/ validate/ tests/` to the
  *hard* gate (E9/F63/F7/F82) is cheap.

> Note: the `roadmap.md` "Test gaps → Logging" item is **stale**: `core/logging.py` is now at 100 % coverage.

---

## 4. Missing functionality

| # | Area | Gap |
|---|------|-----|
| F1 | `task/memory_monitor_task*` | Frequencies are integers ≥ 1 per second, so you **cannot sample or report less than once a second**. Long-running installations need "report every 60 s". Accept a period in seconds (float), or allow fractional frequency. |
| F2 | Timing | An allocation-free, wrap-safe ticks helper in `core` (see P1, D17), shared by all tasks and devices. |
| F3 | Runners | Guaranteed shutdown semantics: let a task's `end` run when the runner stops (D14), for example a final "stop" call, or catching `CancelledError` and awaiting `end`. |
| F4 | `device/button.py` | Configurable long-press duration (hard-coded 2000 ms), pass the click count to `multi_click`, and press/release callbacks. |
| F5 | `core/environment.py` | `is_running_on_linux/mac/windows` are computed but have no accessor. Pin detection only recognises `BLINKA_U2IF`; FT232H, MCP2221 and Raspberry Pi Blinka aren't detected. |
| F6 | `config/configuration.py` | No defaults for `LED_PIN`, `BUTTON_PIN`, `BUTTON_PULLUP`, `PIXELS_COUNT` and similar. The `zero` helpers raise `AttributeError` if a user's `config.py` omits them. |
| F7 | `device/pixels.py` (desktop stub) | The stub discards writes (`__getitem__` returns `[0]`). Storing colours would let tests and desktop runs check animation output. |
| F8 | `network/requests.py` | It connects to WiFi as an **import side effect**, raises at import if settings are missing, has no reconnect, and reads `WIFI_SSID`/`WIFI_PASSWORD` rather than CircuitPython's standard `CIRCUITPY_WIFI_SSID`/`CIRCUITPY_WIFI_PASSWORD`, which would let it reuse the auto-connection. |
| F9 | `device/audio.py` | No looping queue or volume control. Newer CircuitPython can construct `MP3Decoder` from a filename / `open()`, which would remove the bundled `mp3.mp3` placeholder (D9). |
| F10 | `pyproject.toml` | No `dependencies` declared (adafruit libs, psutil, requests), no package data for `mp3.mp3`. |
| F11 | Already on roadmap | One-shot task, servo, ultrasonic, MEMS mic, Pico W CYW LED (no PWM). This affects the validate scripts too, see V3. |

---

## 5. Inconsistencies

- **Docs vs code**
  - `CLAUDE.md` lists 7 submodules but there are 9 (`network`, `zero` missing). It also says
    `validate/` is "not run in CI", but `.github/workflows/python-app.yml` **does** run
    `validate_all.py`.
  - `validate/validation.md` step 6 says to run `validate_performance.py` from Thonny, but
    `validate_performance.py`'s own header says it **cannot** run under Thonny.
    `validate/core/configuration.py` refers to `validate/config.py`, which doesn't exist (it's the
    root `config.py`).
  - `decode_melody` docstring says "separated by a comma" (it's `:`). `I2sAudio` docstring says
    "via PWM". The `Queue` error mentions `I2SAudio`.
  - `changelog.md` has an empty 0.3.6 entry. `roadmap.md` lists a fixed test gap.
- **API / behaviour**
  - Timing sources are mixed: `monotonic()` (float), `monotonic_ns()` and `time()`.
  - Periodic tasks compute intervals with floats; the memory monitor uses integer division.
  - Memory units are MB on desktop vs bytes on device, and desktop "heap" is actually system-wide RAM
    (`psutil.virtual_memory`), not process memory.
  - `None` means "external pull resistor" for `InputPin` but "use config" in `zero`.
  - Error text says "start, run or stop" where the parameters are `begin`, `func`, `end`.
  - Normal cancellation is logged at **ERROR** level in the async runners.
  - `deinit()` idempotence differs between classes (D7).
  - `validate` pixel scripts hard-code 8 pixels instead of `config.PIXELS_COUNT`.
- **Repo hygiene**
  - `requirements.txt` is **UTF-16** encoded (pip copes, but grep/diff/many tools don't).
  - It mixes pinned and unpinned packages.
  - It contains `toml`, which `package.py` doesn't need (it uses stdlib `tomllib`).
  - flake8 is installed only in CI.

---

## 6. `validate/` analysis and suggested improvements

**How it works today:** each `validate/<area>/<x>.py` exposes `execute()`. Area drivers list modules,
and `utils.execute_modules()` runs each one, printing memory before and after. `utils.execute()`
drives a single task with `basic_runner` (or `reliable_runner`) plus `memory_monitor_task` for
`RUNTIME` seconds. `validate/performance/` is a separate harness that chains scripts across soft
reboots with `supervisor.set_next_code_file`.

Problems found:

| # | Issue | Suggestion |
|---|-------|-----------|
| V1 | `validate/core/cpu.py` calls `cpu.info()` 8 times; each call builds a dict and does hardware reads. (The f-string concern originally raised here was withdrawn with D6.) | Call `cpu.info()` once. |
| V2 | `execute_modules()` catches only `MemoryError`. Any other exception (a failed `assert`, a `ValueError` for an unconfigured pin, `ImportError` for `wifi`) **aborts the entire run**, with no summary. | Catch `Exception` per module, record pass/fail/skip, print a final summary table, and exit non-zero on failure (so CI gets a real signal). |
| V3 | Hardware that isn't configured or supported crashes the run: `i2s_audio` with `None` pins, `pwm_pin`/`led` on a Pico W (CYW LED has no PWM), `pwm_audio` passes the string `"none"` as a pin. | Add a `skip_unless(config.X)` helper that prints `SKIP: <reason>` and returns, and use it consistently. |
| V4 | **In CI, `validate_all` runs `network/client.py`, which calls `https://httpbin.org/get` in a tight loop for about 4 s on every push × 3 Python versions.** The `import wifi` guard only exists in `validate_network.py`'s `__main__`, which `validate_all` bypasses. If httpbin is down, CI fails (an unhandled `ConnectionError`). The performance `s_client.py` has the same tight loop. | Make one request (or a rate-limited `periodic_task` at 1 Hz) against the **local** biplane server from `validate/network/server.py`, which is self-contained and also proves the server answers. Skip external calls when `is_running_in_ci()`. |
| V5 | Many scripts only print ("Press the button", "LED will pulse") and assert nothing, so they can't detect regressions on desktop/CI. The task scripts use weak asserts (`task_count > 1`). | Where timing is deterministic, assert ranges. For example, `periodic_task` at 3 Hz with a 1 s delay over 4 s should run about 9 times, so assert 8–11. Count restarts in `reliable_runner` (`> 1`). Assert `Buzzer.playing` transitions, `Melody` note order, and `Queue` emptying. |
| V6 | `reliable_runner` validation raises on **every** cycle, so it logs a warning per iteration (thousands of lines in 4 s on desktop) and formats a traceback each time (D15). | Raise only for the first N calls, then succeed. Assert the restart count. |
| V7 | `del module` in `execute_modules` only removes the loop variable. Modules (and the cptkip modules they imported) stay in `modules` and `sys.modules`, so "Initial memory" for later modules includes everything earlier. | Note the cumulative nature in the output, or `del sys.modules[...]` for cptkip modules a script imported and then `gc.collect()`. The performance harness's reboot-per-script approach already does this properly. |
| V8 | Cycles/sec uses the *requested* `runtime`, not the measured elapsed time (and `finish` adds 0.05 s). The async variant prints `n/a K/s`. | Measure `monotonic()` before and after. Wrap the async task in a counting coroutine so async throughput is reported too. |
| V9 | On desktop, the memory monitor reports **system-wide** RAM in MB, which says nothing about cptkip. | On desktop, report `tracemalloc` current/peak (already half-wired via `PROFILE`) or `psutil.Process().memory_info().rss`. |
| V10 | `REPORT_FREQUENCY = 4` gives 16+ report lines per module per run, and the memory monitor can't go below 1 Hz (F1). | Default to 1 report per run or per second, and print peak at the end. |
| V11 | `validate/utils.execute*` and `validate/performance/task_runner*.execute` are near-duplicates (same `finish`/`continue_func` globals, same cycle maths, same "ake sure" typo). | Share one small harness module. Keep the performance one minimal if its memory numbers must stay comparable. |
| V12 | `performance/c_logging_cptkip.py` says INFO "will appear", but it never loads config, so the level is WARNING and INFO is suppressed. | Set the level explicitly in the script. |
| V13 | Results in `microcontrollers/performance_results/*.txt` are compared by eye. | Add a small parser script that diffs two result files (per-script START/AFTER GC bytes and K/s), so a release can be checked for memory regressions. |
| V14 | No validation for: `Melody` pause/resume/reset, `Queue` pause/resume/cancel, `Buzzer.beeps()`, `OutputPin.toggle`, `Button` multi/long-click counts, `count_limiter`/`duration_limiter`, `zero` helpers. | Add small scripts. The `zero` helpers are the simplest end-to-end check of `config.py` wiring on each board. |
| V15 | `validation.md` says to copy the `.py` sources. Memory figures from source differ from those of the `.mpy` package users actually install. | Document validating against the `package/` (mpy) output, and fix the Thonny contradiction. |

---

## 7. Recommended roadmap

### 0.3.6: correctness patch (small, low-risk)

1. Packaging: fix `packages` (use `[tool.setuptools.packages.find]` + package-data for `mp3.mp3`)
   and the classifier (D1, D2). Add the wheel-import CI check (T7).
2. Fix the confirmed behavioural bugs, each with a regression test: D3/D19 (Melody), D4 (Buzzer
   volume), D5 (zero falsy overrides), D7 (idempotent `deinit`), D11 (Response headers), D20–D23.
3. ~~CircuitPython f-string compatibility (D6/T8)~~: withdrawn, f-strings confirmed working on-device.
4. Stop CI hitting httpbin.org (V4), and make `execute_modules` report pass/fail and exit non-zero (V2).
5. Doc sync: `CLAUDE.md` module list and CI statement, `validation.md`, stale roadmap test-gap entry,
   `requirements.txt` → UTF-8.

### 0.4.0: timing and memory overhaul

1. Introduce a `core` ticks helper (F2) and move all tasks and devices onto it (P1, D17, D18), plus
   integer period maths.
2. Persistent `PWMOut` in `BuzzerPin` (P2). Index-based `triggered_events_task` (P3). Lazy
   `stacktrace` (P5/D15). Integer `Flicker` (P7). Single shared `Trigger` (P10).
3. Async tasks sleep until they're due (P4), using `PERIODIC_LOOP_WAIT_RATIO` or removing it.
4. Memory monitor with a period in seconds (F1).
5. Re-run `validate/performance` on all six boards and commit the diffs (V13) to show the gains.

### 0.4.x: robustness and API polish

1. Runner shutdown semantics so `end` callbacks run (D14/F3). This is a documented behaviour change.
2. Audio: close files, resolve the placeholder path from the module location or drop it (D8–D10, F9).
3. Network: no WiFi connection at import time, support for the `CIRCUITPY_WIFI_*` names, lazy
   `listen_on` defaults (D12, F8). Upstream the biplane fixes (D11, D13).
4. Config defaults (F6), environment accessors and Blinka backends (F5), Button options (F4),
   desktop Pixels stub that keeps state (F7).
5. Validate improvements V3, V5–V12, V14, V15.

### Later (existing roadmap)

Pico W CYW LED fallback to `OutputPin` (also fixes V3 on that board), one-shot task, servo,
ultrasonic, MEMS mic, UART comms, multi-device hierarchy, time-of-day support. Keep checking new
dependencies against the CC BY-NC-SA licence.

---

## 8. Fix tracking

Every finding has one entry below, with a blank line between entries so that PRs touching different
entries merge without conflicts. Each fix PR targets `develop` and is branched from `docs/report-fix-tracking` (this section). Its diff will include this commit until that PR is merged. Each PR updates
only its own entries. Closely coupled findings (same function or same lines) are fixed together in
one PR to avoid conflicting edits. The branch name says which.

Status values: **Open**, **PR open**, **Withdrawn**, **Deferred**, **Question** (maintainer decision, no code change).

### Defects

- **D1** – Open – `fix/packaging`

- **D2** – Open – `fix/packaging`

- **D3** – Open – `fix/melody-reset-first-note`

- **D4** – Open – `fix/buzzer-volume-restarts-tone`

- **D5** – Open – `fix/zero-falsy-overrides`

- **D6** – Withdrawn – nested f-strings confirmed working on-device by the maintainer.

- **D7** – Open – `fix/pin-deinit-idempotent`

- **D8** – Open – `fix/audio-file-handling`

- **D9** – Open – `fix/audio-file-handling`

- **D10** – Open – `fix/audio-file-handling`

- **D11** – Open – `fix/biplane`

- **D12** – Open – `fix/biplane`

- **D13** – Open – `fix/biplane`

- **D14** – Open – `fix/runner-shutdown-end-callbacks`

- **D15** – Open – `perf/lazy-stacktrace`

- **D16** – Open – `fix/duration-limiter-monotonic`

- **D17** – Deferred – adopt the F2 ticks helper in triggered tasks after the task PRs merge (touches the same lines).

- **D18** – Open – `fix/periodic-task-timing`

- **D19** – Open – `fix/melody-reset-first-note`

- **D20** – Open – `fix/memory-report-text`

- **D21** – Open – `fix/melody-note-parsing`

- **D22** – Open – `fix/melody-note-parsing`

- **D23** – Open – `fix/triggered-events-task`

- **D24** – Open – `fix/periodic-task-timing`

- **D25** – Open – `fix/led-getitem-and-parse`

- **D26** – Open – `fix/audio-file-handling`

- **D27** – Open – `fix/triggered-events-task`

- **D28** – Question – is leaving brightness at 0 after `stop_pixels()` intended?

- **D29** – Question – is the ~1.6 % maximum buzzer duty cycle intended?

### Performance

- **P1** – Deferred – adopt the F2 ticks helper across tasks/devices after the task PRs merge (touches the same lines).

- **P2** – Open – `perf/buzzer-pin-persistent-pwm`

- **P3** – Open – `fix/triggered-events-task`

- **P4** – Open – `fix/periodic-task-timing`

- **P5** – Open – `perf/lazy-stacktrace`

- **P6** – Open – `perf/quiet-config-and-defaults`

- **P7** – Open – `perf/flicker-integer-maths`

- **P8** – Open – `perf/cpu-info-single-read`

- **P9** – Open – `fix/led-getitem-and-parse`

- **P10** – Open – `refactor/shared-trigger`

- **P11** – Open – `perf/zero-lazy-animation-imports`

### Tests

- **T1** – Open – `fix/melody-reset-first-note`

- **T2** – Open – `fix/buzzer-volume-restarts-tone`

- **T3** – Open – `fix/zero-falsy-overrides`

- **T4** – Open – `fix/pin-deinit-idempotent`

- **T5** – Open – split across `fix/biplane`, `fix/melody-note-parsing`, `fix/triggered-events-task`

- **T6** – Open – `fix/runner-shutdown-end-callbacks`

- **T7** – Open – `fix/packaging`

- **T8** – Withdrawn – with D6.

- **T9** – Open – `fix/biplane`

- **T10** – Open – `feat/environment-accessors`

- **T11** – Open – `perf/quiet-config-and-defaults`

- **T12** – Open – `fix/periodic-task-timing`

- **T13** – Open – `ci/lint-all-trees`

### Missing functionality

- **F1** – Open – `feat/memory-monitor-slow-rates`

- **F2** – Open – `feat/ticks-helper`

- **F3** – Open – `fix/runner-shutdown-end-callbacks`

- **F4** – Open – `feat/button-options`

- **F5** – Open – `feat/environment-accessors`

- **F6** – Open – `perf/quiet-config-and-defaults`

- **F7** – Open – `feat/pixels-desktop-stub-state`

- **F8** – Open – `feat/network-wifi-settings`

- **F9** – PR open – placeholder file in `fix/audio-file-handling`; looping queue in `feat/audio-queue-loop` – volume control not added (needs audiomixer; decision)

- **F10** – Open – `fix/packaging`

- **F11** – No action – already on `roadmap.md`.

### Inconsistencies (§5)

- **I1** (docs: CLAUDE.md, validation.md, roadmap) – Open – `docs/sync-docs`

- **I2** (requirements.txt encoding/contents) – Open – `docs/sync-docs`

- **I3** (docstrings: decode_melody) – Open – `fix/melody-note-parsing`

- **I4** (docstrings/messages: I2sAudio, Queue) – Open – `fix/audio-file-handling`

- **I5** (error text "start, run or stop") – Open – `refactor/shared-trigger`

- **I6** (cancellation logged at ERROR) – Open – `fix/runner-shutdown-end-callbacks`

- **I7** (validate pixel count hard-coded) – Open – `validate/harness`

- **I8** (mixed timing sources / units) – Deferred – resolved by P1 adoption of F2.

### Validate

- **V1** – Open – `perf/cpu-info-single-read`

- **V2** – Open – `validate/harness`

- **V3** – Open – `validate/harness`

- **V4** – Open – `validate/network-local`

- **V5** – Open – `validate/stronger-task-asserts`

- **V6** – Open – `validate/stronger-task-asserts`

- **V7** – Open – `validate/harness`

- **V8** – Open – `validate/harness`

- **V9** – Open – `validate/harness`

- **V10** – Open – `validate/harness`

- **V11** – Open – `validate/performance-tidy`

- **V12** – Open – `validate/performance-tidy`

- **V13** – Open – `validate/performance-compare`

- **V14** – Open – `validate/new-scripts`

- **V15** – Open – `docs/sync-docs`
