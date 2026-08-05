# Roadmap

## Now

Investigate the "Free: 162464 bytes" value on the validate performance tests and identify how to
maximise it. Specifically investigate the decrease after adding the I2S support.

Investigate a solution to the issue of the on-board LED on a Pico-W being connected to CywPin which
does not support PWM (only digital In/Out) which means the LED examples will fail on the device (and
probably the validation too).

The following functionality is a priority to implement:

* Support for MEMS microphone
* Support for ultrasonic sensors
* Triggered Tasks - async and sync
* lightweight object hierarchy to control multiple devices

## Next

The following functionality is planned to be implemented and is inspired by
`pico-interactive`:

* Move count_limiter, time_limiter and value_flip from test.utilities to task
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

1. `cptkip/config/configuration.py:10-18` — `except ImportError` around config loading also swallows
   `ImportError`s raised from inside a real `config.py`, misreporting genuine failures as "no config
   file found."

## Test gaps

- **Logging**: `core/logging.py` tests leave `LEVEL=WARNING` throughout, so the
  `DEBUG`/`INFO` prefix branches and actual `print()` call are never hit.
- **Sync/async parity untested**: no test confirms `basic_runner`/
  `periodic_task` and their `_async` counterparts behave equivalently for the same parameters; no
  test covers exceptions raised from `periodic_task`'s
  `func`/`begin`/`end`/
  `continue_func` callbacks.