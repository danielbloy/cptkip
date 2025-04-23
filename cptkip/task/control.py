# This file contains common control values that are "hard-coded" and not expected
# to be changed by configuration. The frequency values here are the number of times
# per second that is required.

NS_PER_SECOND = 1_000_000_000

# * * * * *    S C H E D U L E R    * * * * *
SCHEDULER_DEFAULT_FREQUENCY = 30
SCHEDULER_INTERNAL_LOOP_RATIO = 8

# * * * * *    R U N N E R    * * * * *
RUNNER_DEFAULT_CALLBACK_FREQUENCY = 10  # How many times we expect the callback to be called per second.

# * * * * *    L O O P S    * * * * *
# This is expected the sleep interval for async loops.
ASYNC_LOOP_SLEEP_INTERVAL = 0.001
