import gc

print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

import cptkip.core.environment as environment

print('Is running in CI ................. : ', environment.is_running_in_ci())
print('Is running under test ............ : ', environment.is_running_under_test())
print('Is running on a microcontroller .. : ', environment.is_running_on_microcontroller())
print('Is running on a desktop .......... : ', environment.is_running_on_desktop())
print('Are pins available ............... : ', environment.are_pins_available())

print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Load the next file
import supervisor

supervisor.set_next_code_file("/validate/performance/c_logging_adafruit.py")
supervisor.reload()
