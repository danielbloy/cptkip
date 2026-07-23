# Changelog

## 0.1.2 - Beta

Removed CircuitPython device images from the project (the Adafruit libs have been kept). Overhaul of how the on-device
validate scripts work to make it easier to run and identify issues. Added a relatively simple memory monitor task to
assist with on device performance tuning. Some small performance improvements were made to the basic runner. Support was
added for device.py to be loaded after config.py allowing for more flexibility for separating application configuration
from device configuration. Overhauled the validation tests to be more comprehensive but also allow for automated
performance testing.

## 0.1.1 - Beta

Version 0.1.1 contains a small number of bug fixes but mostly contains improvements to the structure of the project
outside the core functionality. The examples have been updated and expanded as well as now running automatically in CI
for each commit.

## 0.1.0 - Beta

Version 0.1.0 contains a broad range of basic functionality covering environment, logging, buttons, LEDs, NeoPixels,
buzzers and PWM audio. Also included are task runners (async and sync). The initial code was based off the
`pico-interactive` project and has been used itself in several coding club projects.
