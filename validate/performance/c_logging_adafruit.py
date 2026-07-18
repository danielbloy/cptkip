import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# noinspection PyUnusedImports
import adafruit_logging as logging

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
import supervisor

supervisor.set_next_code_file("/validate/performance/c_logging_cptkip.py")
supervisor.reload()
