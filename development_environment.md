# Setting up the Development Environment

This page will explain how to setup a local development environment to work on `cptkip`.
The project has been developed using the [PyCharm IDE](https://www.jetbrains.com/pycharm/)
with a VENV for Python with tests written using `pytest` (see
[pytest](https://docs.pytest.org/en/8.2.x/) for more information). Parts of the toolkit are
written to provide functionality that will work in both Python and CircuitPython environments
without requiring access to pins. Those parts of the toolkit can simply be considered typical
Python packages.

Other parts of the toolkit are aimed at executing in an environment that has access to pins.
Because we want to be able to run automated tests against even code that requires pins, the
toolkit shims out the dependencies. There are therefore three primary environment that
`cptkip` will be execute in:

1. A vanilla Python environment with no access to pins; see [Python](#python).
2. A Python environment with access to pins via Blinka; see [Python with Blinka](#python-with-blinka).
3. A CircuitPython environment with native access to pins.

## Python

To test with plain old vanilla Python, simply use PyCharm to setup a new Virtual Environment
(VENV). This project is tested with Python 3.12.

### Stopping the creation of `__pycache__` directories

One annoyance that you may wish to disable is the creation of the `__pycache__` directories as
their presence is a pain when copying the libraries to a microcontroller with limited space.
Amongst other ways, this can be done by adding the following environment variable to the
configuration that you use to run your Tests in PyCharm: `PYTHONDONTWRITEBYTECODE=1`.

See the following
[Stack Overflow article](https://stackoverflow.com/questions/71946178/vs-code-keeps-generating-pycache-files)
for full details.

## Python with Blinka

If you want to have access to real pins when working from a vanilla desktop Python installation,
Blinka is the tool to use (it can also give access to pins on a Raspberry Pi).

Use the Adafruit resources at [CircuitPython Libraries on any Computer with Raspberry Pi Pico](
https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-raspberry-pi-pico/overview)
to setup Blinka. Once setup it'll make it much easier to test CircuitPython code and will be an
invaluable tool when building your own CircuitPython software. Once Blinka is setup, it is trivial
to then run CircuitPython programs directly from within PyCharm using the environment variable:
`BLINKA_U2IF=1`.

Beware that there are some limitations with Blinka that means it cannot be used to test
everything. All of your application code will still need to be tested on the device that
you want to run on to make sure it works in that environment. So far, the main issues
that I have found with Blinka are:

* It is significantly slower that running on the device itself. This is not because your
  computer is slow, it's because of the overhead of calculating and transferring data to
  and from the device. Running your application code on the device is always much faster.
* More than one strand of NeoPixels will not work properly. If you are running a single
  strand of NeoPixels then Blinka works absolutely fine (although it is slower to update than
  running on the device). If however you run multiple strands from different pins then What
  seems to happen is they get combined and output on a single strand. Running your code
  on the device will work fine though (this was infuriating when building the skull path
  nodes).
* Ultrasonic sensors do not give good results. This is possibly related to the speed issue
  but when testing Ultrasonic sensors, I did not get anything like sensible or consistent
  values. Running on the device worked fine though.
* Audio support seems to be unavailable as I was unable to find the appropriate library to
  add to the virtual environment. I did not invest much time into solving this issue as
  the audio is largely handled by CircuitPython and the pico-interactive code is little
  more than a thin layer around it.

## CircuitPython Device

Running on actual hardware provides full access to pins but is not such a rich development
experience. The device also needs to be correctly configured.

From the [CircuitPython](https://circuitpython.org/) website, download the correct version
of CircuitPython for your device. Copy across the `cptkip` packages that you need to the
CircuitPython device. Then finally, copy across the CircuitPython `lib` dependencies that
are required for each `cptkip` package your project uses. The dependencies need to be copied
to the `lib` directory on the CircuitPython device. These dependencies can be found
in `CircuitPython/<version>/lib` using a directory structure corresponding to the `cptkip`
directory structure to make it easy to find only the dependencies you need.

TODO: Add in an example that can be used by a complete novice with no experience of CircuitPython.
