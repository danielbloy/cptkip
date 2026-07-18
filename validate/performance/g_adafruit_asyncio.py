import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# noinspection PyUnusedImports
import asyncio

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
