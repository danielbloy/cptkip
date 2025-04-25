# Memory Usage

The following data is generated from running the various examples on a
Raspberry Pi Pico H device.

| Example                        | Ram at Start                            | RAM at Finish before GC                 | RAM at Finish after GC                  |
|--------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| `cptkip.core.memory.py`        | Used: 12,832 bytes, Free: 15,4528 bytes | Used: 14,240 bytes, Free: 153,120 bytes | Used: 12,928 bytes, Free: 154,432 bytes |
| `cptkip.task.simple_runner.py` | Used: 28,416 bytes, Free: 139,264 bytes | Used: 61,600 bytes, Free: 106,080 bytes | Used: 32,208 bytes, Free: 135,472 bytes |
| `manual_runner.py`             |                                         |                                         |                                         |
