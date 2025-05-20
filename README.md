# Circuit Python Toolkit for Interactive Projects (CPTKIP)

Please see my website [Code Club Adventures](http://codeclubadventures.com/) for more coding materials.

## Origins

For details of the origins of this project, see [pico-interactive](https://github.com/danielbloy/pico-interactive).
This project is expected to be significantly different in structure and principles from the
original project, so I've decided to make it and new project rather than a version 2 of
[pico-interactive](https://github.com/danielbloy/pico-interactive) which I will continue to
support as I use it in lots of my existing projects.

Rather than focus on a single universal framework (aimed primarily at Raspberry Pi Pico based
boards), this project aims to be more of a toolkit that supports a wide range of CircuitPython
divides as well as standard Python on a computer. It is designed to be both simpler to use and
simpler to extend/maintain than `pico-interactive` which requires a fair bit more boilerplate
to add new functionality. I have also tried to reduce the memory demands of using some of the
lower level modules such as logging which can be found in the `core` module.

## Overview

For information on how to setup a development environment, see
[development_environment.md](development_environment.md).

The structure of the project will be the following modules (listed in order of importance):

* core - required for every `cptkip` project as it provides information about execution
  environment, memory and logging. It has no dependencies on other `cptkip` packages.
* config - provides overridable configuration properties.
* cpu - provides information about the CPU and provides some operations.
* task - provides async thread runners and task scheduling that works across all supported
  platforms (CircuitPython and Python).
* pin - provides an abstraction layer to support environments with no physical pins.
* device - provides abstractions for hardware components.
* animation - provides additional animations such as `Flicker`.
* sound - provides support for playing sound through buzzers and speakers.

The packages and their dependencies are illustrated in the table below.

|                    | `cptkip.core` | `cptkip.config` | `cptkip.cpu` | `cptkip.pin` | `cptkip.task` | `cptkip.device` |
|--------------------|:-------------:|:---------------:|:------------:|:------------:|:-------------:|:---------------:|
| `cptkip.core`      |      n/a      |                 |              |              |               |                 |
| `cptkip.config`    |      yes      |       n/a       |              |              |               |                 |
| `cptkip.cpu`       |      Yes      |                 |     n/a      |              |               |                 |
| `cptkip.pin`       |      Yes      |                 |              |     n/a      |               |                 |
| `cptkip.task`      |      Yes      |                 |              |              |      n/a      |                 |
| `cptkip.device`    |      Yes      |                 |              |     Yes      |               |       n/a       |
| `cptkip.animation` |               |                 |              |              |               |                 |

## Roadmap

The following functionality remains to be ported over from `pico-interactive`

* Periodic tasks - sync version
* Safe Runner - async and non async
* Triggered Task - async and non async
* Timed Events Task - async and non async
* One time on/off task - async and non async
* Buzzer - device test
* LED - device test
* Melody - device test
* Melody - reduce memory requirements
* Melody - consider reworking code to use
  audiopwmio: https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
* Ultrasonic - port and test

The following functionality remains to be implemented:

* Migrate to a lighter weight, faster and async HTTP server stack such as [Biplane](https://github.com/Uberi/biplane).
  This will likely involve a notable reworking of the network code.
* Add time of day support.
* Add support for communications between Picos using UART and possible 1-wire support.
* Include a version/build number in the library and add it in automatically.
* Compile to `.mpy` files and add an official release process.

### Hardware Support

* Remove most of the existing content of the `hardware` section, moving it to the `Halloween` repository.
* Add a section for each explicitly supported board in the `hardware` with examples to make it as
  simple as possible for newcomers to get up and running with off the shelf hardware.
* Add a section for the "Christmas Board" -> "Demo Board" as an example of a trivial homemade board.
* Remove the `demo` section, placing the example under `boards/demo_board`.
* Document the best way to use `pico-interactive` based on available device RAM/board classification
  (i.e. Network uses so much RAM that it is difficult for a Pico 1 to do much else).
* Add full support hardware test cycle for Pi Zero 2, Pi 3A/3A, Pi 400/4B boards, including setup documentation.

## License

All materials provided in this project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International License. To view a copy of this license, visit
<https://creativecommons.org/licenses/by-nc-sa/4.0/>.

In summary, this means that you are free to:

* **Share** — copy and redistribute the material in any medium or format.
* **Adapt** — remix, transform, and build upon the material.

Provided you follow these terms:

* **Attribution** — You must give appropriate credit , provide a link to the license, and indicate if changes were made.
  You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* **NonCommercial** — You may not use the material for commercial purposes.
* **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the
  same license as the original.
