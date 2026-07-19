#
# This script is not run as part of validate all as it performs a series of
# soft reboots of the device, running a different script each time. This script
# also cannot be run using Thonny as Thonny will just intercept the REPL each
# it tries to reboots. Therefore, this script needs to be run by connecting to
# the device over a serial connection, dropping to the REPL and then importing
# this file like this:
#     import validate.validate_performance
#
# A series of scripts will then run with each tracking the memory and performance
# characteristics of the device and the cptkip framework (plus a few adafruit
# modules for good measure).
#
from cptkip.core.environment import is_running_on_microcontroller

if is_running_on_microcontroller():
    from validate.performance.script_runner import execute_next_script

    execute_next_script()
