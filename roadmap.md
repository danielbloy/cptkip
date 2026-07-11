# Roadmap

## Now

The following functionality is a priority to implement and inspired by `pmpge`:

* Improvements to loading configuration, specifically for device specific config
* lightweight object hierarchy to control multiple devices
* Continued evolement of the project structure with an improved validation process

The following functionality is a priority to implement and is inspired by `pico-interactive`:

* Network stack - ideally integrating a light-weight, fast and async HTTP server stack such
  as [Biplane](https://github.com/Uberi/biplane).
* Triggered Tasks - async and sync
* Ultrasonic sensors

The following functionality is a priority to implement:

* Support for I2S audio
* Support for MEMS microphone

## Next

The following functionality is planned to be implemented and is inspired by `pico-interactive`:

* Safe Runner - async and sync
* Timed Events Task - async sync
* One time on/off task - async and sync

## Later

The following functionality remains to be implemented:

* Add support for communications between Picos using UART and possible 1-wire support.
* Include a version/build number in the library and add it in automatically.
* Add time of day support.
* Melody - consider reworking code to use
  audiopwmio: https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
* Compile to `.mpy` files and add an official release process.

## Issues

### Issues to consider when reworking configuration

1. `cptkip/config/configuration.py:5-20` — `import cptkip.core.logging as logging` can be
   silently shadowed by `from config import *` if the user's `config.py` imports anything
   named `logging` (e.g. stdlib `logging`), causing an `AttributeError` at import time.
2. `cptkip/config/configuration.py:10-18` — `except ImportError` around config loading
   also swallows `ImportError`s raised from inside a real `config.py`, misreporting
   genuine failures as "no config file found."

## Test gaps

- **Logging**: `core/logging.py` tests leave `LEVEL=WARNING` throughout, so the
  `DEBUG`/`INFO` prefix branches and actual `print()` call are never hit.
- **Sync/async parity untested**: no test confirms `basic_runner`/`periodic_task` and
  their `_async` counterparts behave equivalently for the same parameters; no test covers
  exceptions raised from `periodic_task`'s `func`/`begin`/`end`/`continue_func` callbacks.
- **Boundary/invalid input untested**:
    - `buzzer_pin`/`pwm_pin` volume clamping outside [0,1]
    - negative frequency in `play()`
    - `led.py` brightness clamping outside [0,1]
    - negative in `buzzer.beeps(0)`