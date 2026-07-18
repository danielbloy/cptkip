import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

import cptkip.core.memory as memory

memory.report_memory_usage()
memory.report_memory_usage_and_free()

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
import supervisor

supervisor.set_next_code_file("/validate/performance/e_configuration.py")
supervisor.reload()
