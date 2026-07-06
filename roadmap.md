# Roadmap

## Now

The following functionality is a priority to implement and inspired by `pmpge`:

* Improvements to loading configuration, specifically for device specific config
* lightweight object hierarchy to control multiple devices
* Continued evolement of the project structure with an improved validation process

The following functionality is a priority to implement and is inspired by `pico-interactive`:

* Network stack - ideally integrating a light-weight, fast and async HTTP server stack such as [Biplane](https://github.com/Uberi/biplane).
* Triggered Tasks - async and sync
* Ultrasonic sensors

The following functionality is a priority to implement:

* Support for I2S audio

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
