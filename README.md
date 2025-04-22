# Circuit Python Toolkit for Interactive Projects (CPTKIP)

Please see my website [Code Club Adventures](http://codeclubadventures.com/) for more coding materials.

## Origins

For details of the origins of this project, see [pico-interactive](https://github.com/danielbloy/pico-interactive).
This project is expected to be significantly different in structure and principles from the original
project, so I've decided to make it and new project rather than a version 2 of
[pico-interactive](https://github.com/danielbloy/pico-interactive) which I will continue to support
as I use it in lots of my existing projects.

Rather than focus on a single universal framework (aimed primarily at Raspberry Pi Pico based
boards), this project aims to be more of a toolkit that supports a wide range of CircuitPython divides
as well as standard Python on a computer. It is designed to be modular so you can select the specific
bits of functionality you need with a pick and mix approach. One of the principles behind this approach
is to reduce the memory overheads of using the toolkit as well as make it more flexible.

## Overview

The initial structure of the project will be the following modules:

* core - required for every `cptkip` project as it provides information about execution environment
  and logging. It has no dependencies on other cptkip packages.
* task - provies an async thread runner that works across all supported platforms (CircuitPython and
  Python). Has a dependency on `core`.

## How To

### Setup Blinka

### Setup PyCharm and venv

### Setup and run tests in Pycharm

This is done on a desktop.

### Setup device and run tests

The mule device will be a Pico W.

Run each module in a specific order to validate there are no dependencies other than those documented.

## Migrated roadmap

Below you will find the proposed roadmap of functionality that I was planning to build into
the version 2 of the `pico-interactive` project before I decided to spin it out into its own
project. This is all subject to change and no timelines are provided.

The following are the set of changes I plan to make compared
to [pico-interactive](https://github.com/danielbloy/pico-interactive).
These changes are written with respect to that project and I'll be updating here are I go along.

### Structural Changes

* Remove the adafruit_animations from the polyfills. These can be imported directly and it will
  help simplify the code. The polyfills are really only needed for the core framework code and
  the animations aren't. Due to this being a breaking change, I will be bumping up to the next
  major version.
* Migrate to a lighter weight, faster and async HTTP server stack such as [Biplane](https://github.com/Uberi/biplane).
  This will likely involve a notable reworking of the network code.

### Testing and Documentation Improvements

* Modify the `test/on_device` programs to use configuration to make testing multiple devices easier.
* Add instructions on each `test/on_device` program to make it easier to know what to expect.
* Move the `tests/on_device` section to `examples` and provide some documentation on how to run on
  different devices.
* Have a "test all" program that works within Pico 1 memory limits and one that works with Pico 2.
* Ensure device tests can run with Blinka too.

### Hardware Support

* Remove most of the existing content of the `hardware` section, moving it to the `Halloween` repository.
* Add a section for each explicitly supported board in the `hardware` with examples to make it as
  simple as possible for newcomers to get up and running with off the shelf hardware.
* Add a section for the "Christmas Board" -> "Demo Board" as an example of a trivial homemade board.
* Remove the `demo` section, placing the example under `boards/demo_board`.
* Document the best way to use `pico-interactive` based on available device RAM/board classification
  (i.e. Network uses so much RAM that it is difficult for a Pico 1 to do much else).
* Add full support hardware test cycle for Pi Zero 2, Pi 3A/3A, Pi 400/4B boards, including setup documentation.

### Simplification and Optimisation

* Investigate optimising task creation to remove unnecessary nested tasks; hopefully to remove memory
  footprint.
* Look to simplify the framework further to make it easier to use.

### Enhancements and Bug Fixes

* Include version number in the `pico-interactive` library and add it in automatically.
* Compile to `.mpy` files and add an official release process.
* Support using board.LED for an LED in tests (so it works with Pico 2 W)
* Add time of day support.
* Support JSON in messages.
* Add support for communications between Picos using UART and possible 1-wire support.

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
