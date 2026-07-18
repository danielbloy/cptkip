import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

import cptkip.config.configuration as config

print('Test value ... :', config.TEST_VALUE)
print('Test string .. :', config.TEST_STRING)
print('Debug ........ :', config.DEBUG)

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
import supervisor

supervisor.set_next_code_file("/validate/performance/f_cpu.py")
supervisor.reload()
