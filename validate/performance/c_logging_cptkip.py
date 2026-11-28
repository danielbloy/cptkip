import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

import cptkip.core.logging as log

# The configuration (and so its LOG_LEVEL) is deliberately not loaded by this script,
# so set the level the messages below describe explicitly.
log.set_log_level(log.INFO)

log.critical('This critical text will appear with log level info')
log.error('This error text will appear with log level info')
log.warn('This warning text will appear with log level info')
log.info('This information text will appear with log level info')
log.debug('This debug text will NOT appear with log level info')

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
