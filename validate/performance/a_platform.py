import gc
import sys

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

major = sys.implementation.version[0]
minor = sys.implementation.version[1]
micro = sys.implementation.version[2]
version = "v" + str(major) + "." + str(minor) + "." + str(micro)

print("Running on:", sys.implementation.name, version, sys.implementation._machine)

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
import supervisor

supervisor.set_next_code_file("/validate/performance/b_environment.py")
supervisor.reload()
