# Memory Usage

The following data is generated from running the various examples on a
Raspberry Pi Pico H device.

| Example                                                                         | Ram at Start                            | RAM at Finish before GC                 | RAM at Finish after GC                  |
|---------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| `cptkip.core.memory.py`                                                         | Used: 12,832 bytes, Free: 15,4528 bytes | Used: 14,240 bytes, Free: 153,120 bytes | Used: 12,928 bytes, Free: 154,432 bytes |
| `cptkip.task.simple_runner.py`                                                  | Used: 28,416 bytes, Free: 139,264 bytes | Used: 61,600 bytes, Free: 106,080 bytes | Used: 32,208 bytes, Free: 135,472 bytes |
| `cptkip.task.simple_runner.py` with unrequired code removed from `scheduler.py` | Used: 25,664 bytes, Free: 142,016 bytes | Used: 43,296 bytes, Free: 124,384 bytes | Used: 27,552 bytes, Free: 140,128 bytes |
| `cptkip.task.simple_runner.py` with unrequired code moved from `triggerable.py` | Used: 25,680 bytes, Free: 142,000 bytes | Used: 43,264 bytes, Free: 124,416 bytes | Used: 27,568 bytes, Free: 140,112 bytes |
| `manual_runner.py`                                                              |                                         |                                         |                                         |

## Lessons learned

* Prefer small module with only a few items of functionality over larger modules to save RAM.
* 