# Changelog

## 0.2.2 - Beta

Added support for triggered tasks (sync and async).

## 0.2.1 - Beta

Contains a minor change to the output of the details from the memory logging. No functional changes.

## 0.2.0 - Beta, breaking change to for `cptkip/device/pwm_audio.py`

Renamed `cptkip/device/pwm_audio.py` to `cptkip/device/audio.py` as it contains support for I2S
audio as well as PWM audio. This is a breaking change. The Audio class no longer takes a pin object
(for PWM) but an audio_out so that it can be used with PWM or I2S. Two convenience functions
(`PwmAudio` and `I2sAudio`) have been added to make it trivial to create the correct audio type.
Existing code can easily be migrated through a simple change to the import statement from:

```python
from cptkip.device.pwm_audio import Audio, Queue
```

to

```python
from cptkip.device.audio import PwmAudio as Audio, Queue
```

Implemented the network stack, using a vendored version of Biplane for the server and abstracted the
requests package to provide portability between Python and circuitPython. Also introduced
`cptkip.zero` to make it simpler to use devices using the standard conventions used in the default
configuration file.

## 0.1.3 - Beta

Used claude to do an analysis of the code base, making a small range of bug fixes and documentation
updates whilst maintaining backwards compatibility.

## 0.1.2 - Beta

Removed CircuitPython device images from the project (the Adafruit libs have been kept). Overhaul of
how the on-device validate scripts work to make it easier to run and identify issues. Added a
relatively simple memory monitor task to assist with on device performance tuning. Some small
performance improvements were made to the basic runner. Support was added for device.py to be loaded
after config.py allowing for more flexibility for separating application configuration from device
configuration. Overhauled the validation tests to be more comprehensive but also allow for automated
performance testing.

## 0.1.1 - Beta

Version 0.1.1 contains a small number of bug fixes but mostly contains improvements to the structure
of the project outside the core functionality. The examples have been updated and expanded as well
as now running automatically in CI for each commit.

## 0.1.0 - Beta

Version 0.1.0 contains a broad range of basic functionality covering environment, logging, buttons,
LEDs, NeoPixels, buzzers and PWM audio. Also included are task runners (async and sync). The initial
code was based off the
`pico-interactive` project and has been used itself in several coding club projects.
