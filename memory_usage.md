# Memory Usage

The following data is generated from running the various examples on a
Raspberry Pi Pico H device running CircuitPython 9.2.7 to assess the
memory demands of the various packages.

## Vanilla Circuit Python

Running the following script which is just output RAM usage with the simplest code footprint possible.

```python
import gc

print(f"MEMORY USAGE:")
print(f"HEAP: Allocated: {gc.mem_alloc()} bytes, Free: {gc.mem_free()} bytes")

# Code under test goes here.

print(f"MEMORY USAGE: before gc")
print(f"HEAP: Allocated: {gc.mem_alloc()} bytes, Free: {gc.mem_free()} bytes")
gc.collect()
print(f"MEMORY USAGE: after gc")
print(f"HEAP: Allocated: {gc.mem_alloc()} bytes, Free: {gc.mem_free()} bytes")
```

| Vanilla Circuit Python  |                                      |
|-------------------------|--------------------------------------|
| Ram at Start            | Used: 656 bytes, Free: 167,024 bytes |
| RAM at Finish before GC | Used: 832 bytes, Free: 166,848 bytes |
| RAM at Finish after GC  | Used: 688 bytes, Free: 166,992 bytes |

Running the above script with the following code under test indicates the cost of adafruit logging, almost 8Kb! Ouch.

```python
import adafruit_logging as logging
```

| Vanilla Circuit Python  |                                        |
|-------------------------|----------------------------------------|
| Ram at Start            | Used:   976 bytes, Free: 166,704 bytes |
| RAM at Finish before GC | Used: 8,272 bytes, Free: 15,9088 bytes |
| RAM at Finish after GC  | Used: 8,272 bytes, Free: 15,9088 bytes |

## `cptkip.core`

| `cptkip.core.environment.py` | `examples/cptkip/core/environment.py` with the code from the Vanilla example above to report RAM |
|------------------------------|--------------------------------------------------------------------------------------------------|
| Ram at Start                 | Used: 1,520 bytes, Free: 166,160 bytes                                                           |
| RAM at Finish before GC      | Used: 3,328 bytes, Free: 164,032 bytes                                                           |
| RAM at Finish after GC       | Used: 3,008 bytes, Free: 164,352 bytes                                                           |

| `cptkip.core.log.py`    | `examples/cptkip/core/logging.py` with removal of adafruit_logging |
|-------------------------|--------------------------------------------------------------------|
| Ram at Start            | Used: 2,032 bytes, Free: 165,648 bytes                             |
| RAM at Finish before GC | Used: 4,800 bytes, Free: 162,560 bytes                             |
| RAM at Finish after GC  | Used: 4,480 bytes, Free: 162,880 bytes                             |

| `cptkip.core.memory.py` | `examples/cptkip/core/memory.py`       |
|-------------------------|----------------------------------------|
| Ram at Start            | Used: 4,704 bytes, Free: 162,656 bytes |
| RAM at Finish before GC | Used: 4,944 bytes, Free: 162,416 bytes |
| RAM at Finish after GC  | Used: 4,784 bytes, Free: 162,576 bytes |

## Experiments with the old framework

Some tests were run using the old runner framework which is a bit memory hungry to see how much it can potentially be
optimised.

Using the original logging framework.

| Example                                                                         | Ram at Start                            | RAM at Finish before GC                 | RAM at Finish after GC                  |
|---------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| `cptkip.task.simple_runner.py`                                                  | Used: 28,416 bytes, Free: 139,264 bytes | Used: 61,600 bytes, Free: 106,080 bytes | Used: 32,208 bytes, Free: 135,472 bytes |
| `cptkip.task.simple_runner.py` with unrequired code removed from `scheduler.py` | Used: 25,664 bytes, Free: 142,016 bytes | Used: 43,296 bytes, Free: 124,384 bytes | Used: 27,552 bytes, Free: 140,128 bytes |
| `cptkip.task.simple_runner.py` with unrequired code moved to `triggerable.py`   | Used: 25,680 bytes, Free: 142,000 bytes | Used: 43,264 bytes, Free: 124,416 bytes | Used: 27,568 bytes, Free: 140,112 bytes |
| `manual_runner.py`                                                              | Used: 24,672 bytes, Free: 142,112 bytes | Used: 29,536 bytes, Free: 137,248 bytes | Used: 27,872 bytes, Free: 138,912 bytes |

Using the memory optimised logging framework.

| Example                                                                       | Ram at Start                            | RAM at Finish before GC                 | RAM at Finish after GC                  |
|-------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| `cptkip.task.simple_runner.py` with unrequired code moved to `triggerable.py` | Used: 18,336 bytes, Free: 149,344 bytes | Used: 38,896 bytes, Free: 128,784 bytes | Used: 20,224 bytes, Free: 147,456 bytes |
| `manual_runner.py`                                                            | Used: 17,552 bytes, Free: 149,232 bytes | Used: 24,256 bytes, Free: 142,528 bytes | Used: 20,816 bytes, Free: 145,968 bytes |

## Lessons learned

* Prefer small module with only a few items of functionality over larger modules to save RAM.
* F strings are expensive in temporary memory usage, it's more efficient to

## Notes

* Logging is expensive when using `adadfruit_logging` so the built-in logging package as part of `cptkip.core`
  has been simplified to remove all dependencies to use far less RAM. If more complex logging is required then
  use the `cptkip.logging` package which has an identical interface but uses the full logging frameworks.
