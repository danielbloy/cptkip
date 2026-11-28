# Validating on a device

The validation scripts are designed to be run on a CircuitPython device to
validate both the correctness of CPTKIP but also validate overall performance.
The validation tests require a human to check the results so have some
interactivity. There is also a `validate_all.py` script which runs all tests
(except the performance scripts, see below).

`validate_all.py` is also run on a desktop as the last step of CI. There are no
pins on a desktop so the hardware scripts only exercise the desktop stand-ins; it
mainly catches scripts that raise.

## Setting up the device

1. Copy the `cptkip` directory to the root of the device. Either copy the source
   `cptkip` directory, or (recommended for meaningful memory figures) the compiled
   `.mpy` version produced by `package.py` in `package/cptkip`, which is what users
   normally install and uses noticeably less RAM.
2. Copy the entire `validate` directory to the root of the device.
3. Create a `lib` directory in the root of the device.
4. Copy the `config.py` file from the root of the repository (not the `cptkip` package
   directory - it is a sibling of it, not part of it) to the root of your device.
5. Copy across the contents of `CircuitPython/<version>/lib` into the `lib`
   directory on the device for your version of CircuitPython.
6. For the network scripts, add `WIFI_SSID` and `WIFI_PASSWORD` to `settings.toml`
   on the device.

## Running the functional validation

Use Thonny (or the REPL) to run `validate_all.py`, or one of the area scripts such as
`validate_core.py`, `validate_task.py`, `validate_pin.py`, `validate_device.py`,
`validate_animation.py` or `validate_network.py`.

## Running the performance validation

`validate_performance.py` **cannot** be run from Thonny: it performs a series of soft
reboots (running a different script each time) and Thonny intercepts the REPL on each
reboot. Instead, connect to the device over a serial connection, drop to the REPL and run:

```python
import validate.validate_performance
```

The results can be compared with those in `microcontrollers/performance_results`.
