# Memory Usage

The following data is generated from running the various examples on a
Pimoroni Tiny 2040 device running CircuitPython 9.2.7 to assess the
memory demands of the various packages.

## Vanilla Circuit Python

Running the following script which is just output RAM usage with the simplest code footprint possible.

```python
import gc

print("START: Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

# Code under test goes here.

print("BEFORE GC: Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
gc.collect()
print("AFTER GC: Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
```

| Vanilla Circuit Python  |                                      |
|-------------------------|--------------------------------------|
| Ram at Start            | Used: 640 bytes, Free: 171,136 bytes |
| RAM at Finish before GC | Used: 840 bytes, Free: 171,13 bytes  |
| RAM at Finish after GC  | Used: 640 bytes, Free: 171,13 bytes  |

## The `adafruit_logging` library

Running the above script with the following code under test indicates the cost of `adafruit_logging`, almost 8Kb! Ouch.

```python
import adafruit_logging as logging
```

| `adafruit_logging`      |                                        |
|-------------------------|----------------------------------------|
| Ram at Start            | Used:   848 bytes, Free: 170,928 bytes |
| RAM at Finish before GC | Used: 8,016 bytes, Free: 163,504 bytes |
| RAM at Finish after GC  | Used: 8,016 bytes, Free: 163,504 bytes |

## `cptkip.core.environment.py`

Code under test:

```python
import cptkip.core.environment as environment

print('Is running in CI ................. : ', environment.is_running_in_ci())
print('Is running under test ............ : ', environment.is_running_under_test())
print('Is running on a microcontroller .. : ', environment.is_running_on_microcontroller())
print('Is running on a desktop .......... : ', environment.is_running_on_desktop())
print('Are pins available ............... : ', environment.are_pins_available())
```

| `cptkip.core.environment.py` |                                        |
|------------------------------|----------------------------------------|
| Ram at Start                 | Used: 1,376 bytes, Free: 170,400 bytes |
| RAM at Finish before GC      | Used: 2,912 bytes, Free: 168,608 bytes |
| RAM at Finish after GC       | Used: 2,912 bytes, Free: 168,608 bytes |

## `cptkip.core.logging.py`

Code under test:

```python
import cptkip.core.logging as log

log.critical('This critical text will appear with log level info')
log.error('This error text will appear with log level info')
log.warn('This warning text will appear with log level info')
log.info('This information text will appear with log level info')
log.debug('This debug text will NOT appear with log level info')
```

| `cptkip.core.logging.py` |                                        |
|--------------------------|----------------------------------------|
| Ram at Start             | Used: 1,312 bytes, Free: 170,464 bytes |
| RAM at Finish before GC  | Used: 3,856 bytes, Free: 167,664 bytes |
| RAM at Finish after GC   | Used: 3,856 bytes, Free: 167,664 bytes |

## `cptkip.core.memory.py`

Code under test:

```python
import cptkip.core.memory as memory

memory.report_memory_usage()
memory.report_memory_usage_and_free()
```

| `cptkip.core.memory.py` |                                        |
|-------------------------|----------------------------------------|
| Ram at Start            | Used: 864 bytes, Free: 170,912 bytes   |
| RAM at Finish before GC | Used: 4,800 bytes, Free: 166,720 bytes |
| RAM at Finish after GC  | Used: 4,608 bytes, Free: 166,912 bytes |

## `cptkip.config/configuration.py`

Code under test (using the config file form `examples`):

```python
import cptkip.config.configuration as config

print('Test value ... :', config.TEST_VALUE)
print('Test string .. :', config.TEST_STRING)
print('Debug ........ :', config.DEBUG)
```

| `cptkip.config.configuration.py` |                                        |
|----------------------------------|----------------------------------------|
| Ram at Start                     | Used: 1,040 bytes, Free: 170,736 bytes |
| RAM at Finish before GC          | Used: 4,688 bytes, Free: 166,832 bytes |
| RAM at Finish after GC           | Used: 4,688 bytes, Free: 166,832 bytes |

## `cptkip.cpu.cpu.py`

Code under test:

```python
import cptkip.cpu.cpu as cpu

cpu.info()
```

| `cptkip.cpu.cpu.py`     |                                        |
|-------------------------|----------------------------------------|
| Ram at Start            | Used: 848 bytes, Free: 170,928 bytes   |
| RAM at Finish before GC | Used: 2,992 bytes, Free: 168,528 bytes |
| RAM at Finish after GC  | Used: 2,944 bytes, Free: 168,576 bytes |

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
* F strings are expensive in temporary memory usage, it's more efficient to use `print()` with
  multiple arguments.

## Notes

* Logging is expensive when using `adadfruit_logging` so the built-in logging package as part of `cptkip.core`
  has been simplified to remove all dependencies to use far less RAM. If more complex logging is required then
  use the `cptkip.logging` package which has an identical interface but uses the full logging frameworks.
