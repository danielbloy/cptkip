# This file contains common control values that are "hard-coded" and not expected
# to be changed by configuration. The frequency values here are the number of times
# per second that is required.

NS_PER_SECOND = 1_000_000_000

# For loops that are periodic, this ratio determines the sleep time to period
# ratio. For example, a value of 8 means the sleep time is 1/8 of the period.
# Larger numbers give a more accurate period but also require more CPU time.
PERIODIC_LOOP_WAIT_RATIO = 8

# This is expected the sleep interval for async loops.
ASYNC_LOOP_SLEEP_INTERVAL = 0.001

# These properties are used to control the default ports and timeouts used for
# networking.
SEND_MESSAGE_TIMEOUT = 2  # seconds
NETWORK_PORT_MICROCONTROLLER = 80
NETWORK_PORT_DESKTOP = 5001
