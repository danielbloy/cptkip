# This file contains common control values that are "hard-coded" and not expected
# to be changed by configuration. The frequency values here are the number of times
# per second that is required.

NS_PER_SECOND = 1_000_000_000

# For loops that are periodic, this ratio determines the sleep time to period
# ratio. For example, a value of 8 means the sleep time is 1/8 of the period.
# Larger numbers give a more accurate period but also require more CPU time.
PERIODIC_LOOP_WAIT_RATIO = 8
