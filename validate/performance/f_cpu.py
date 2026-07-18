import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

import cptkip.cpu.cpu as cpu

cpu.info()

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
import supervisor

supervisor.set_next_code_file("/validate/performance/g_adafruit_asyncio.py")
supervisor.reload()
