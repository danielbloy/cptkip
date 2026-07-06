# Roadmap

The following functionality is a priority to implement and inspired by 'pmpge':

* Improvements to loading configuration, specifically for device specific config.
* lightweight object hierarchy control multiple devices
* Improved project structure
* Improved validation process

The following functionality is a priority to implement and is inspired by `pico-interactive`:

* Network stack - ideally igrating to a light-weight, fast and async HTTP server stack such as [Biplane](https://github.com/Uberi/biplane).
* Triggered Task - async and non async
* Ultrasonic - port and test

The following functionality is planned to be implemented and is inspired by `pico-interactive`:

* Safe Runner - async and non async
* Timed Events Task - async and non async
* One time on/off task - async and non async


The following functionality remains to be implemented:

* Add support for communications between Picos using UART and possible 1-wire support.
* Include a version/build number in the library and add it in automatically.
* Add time of day support.
* Melody - consider reworking code to use
  audiopwmio: https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
* Compile to `.mpy` files and add an official release process.
