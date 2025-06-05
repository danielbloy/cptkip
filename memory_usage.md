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

| Vanilla Circuit Python  |                 |
|-------------------------|-----------------|
| Ram at Start            | Used: 544 bytes |
| RAM at Finish before GC | Used: 544 bytes |
| RAM at Finish after GC  | Used: 544 bytes |

## The `adafruit_logging` library

Running the above script with the following code under test indicates the cost of `adafruit_logging`, almost 8Kb! Ouch.

```python
import adafruit_logging as logging
```

| `adafruit_logging`      |                   |
|-------------------------|-------------------|
| Ram at Start            | Used:   848 bytes |
| RAM at Finish before GC | Used: 8,016 bytes |
| RAM at Finish after GC  | Used: 8,016 bytes |

## `cptkip/core/environment.py`

Code under test:

```python
import cptkip.core.environment as environment

print('Is running in CI ................. : ', environment.is_running_in_ci())
print('Is running under test ............ : ', environment.is_running_under_test())
print('Is running on a microcontroller .. : ', environment.is_running_on_microcontroller())
print('Is running on a desktop .......... : ', environment.is_running_on_desktop())
print('Are pins available ............... : ', environment.are_pins_available())
```

| `cptkip/core/environment.py` |                   |
|------------------------------|-------------------|
| Ram at Start                 | Used: 1,376 bytes |
| RAM at Finish before GC      | Used: 2,912 bytes |
| RAM at Finish after GC       | Used: 2,912 bytes |

## `cptkip/core/logging.py`

Code under test:

```python
import cptkip.core.logging as log

log.critical('This critical text will appear with log level info')
log.error('This error text will appear with log level info')
log.warn('This warning text will appear with log level info')
log.info('This information text will appear with log level info')
log.debug('This debug text will NOT appear with log level info')
```

| `cptkip/core/logging.py` |                   |
|--------------------------|-------------------|
| Ram at Start             | Used: 1,312 bytes |
| RAM at Finish before GC  | Used: 3,856 bytes |
| RAM at Finish after GC   | Used: 3,856 bytes |

## `cptkip/core/memory.py`

Code under test:

```python
import cptkip.core.memory as memory

memory.report_memory_usage()
memory.report_memory_usage_and_free()
```

| `cptkip/core/memory.py` |                   |
|-------------------------|-------------------|
| Ram at Start            | Used: 864 bytes   |
| RAM at Finish before GC | Used: 4,800 bytes |
| RAM at Finish after GC  | Used: 4,608 bytes |

## `cptkip/config/configuration.py`

Code under test (using the config file form `examples`):

```python
import cptkip.config.configuration as config

print('Test value ... :', config.TEST_VALUE)
print('Test string .. :', config.TEST_STRING)
print('Debug ........ :', config.DEBUG)
```

| `cptkip/config/configuration.py` |                   |
|----------------------------------|-------------------|
| Ram at Start                     | Used: 1,040 bytes |
| RAM at Finish before GC          | Used: 5,200 bytes |
| RAM at Finish after GC           | Used: 5,200 bytes |

## `cptkip/cpu/cpu.py`

Code under test:

```python
import cptkip.cpu.cpu as cpu

cpu.info()
```

| `cptkip/cpu/cpu.py`     |                   |
|-------------------------|-------------------|
| Ram at Start            | Used: 848 bytes   |
| RAM at Finish before GC | Used: 3,056 bytes |
| RAM at Finish after GC  | Used: 3,008 bytes |

## `asyncio`

Code under test:

```python
import asyncio
```

| `asyncio`               |                   |
|-------------------------|-------------------|
| Ram at Start            | Used: 848 bytes   |
| RAM at Finish before GC | Used: 8,192 bytes |
| RAM at Finish after GC  | Used: 8,192 bytes |

## `cptkip/task/basic_runner.py`

Code under test:

```python
import time
import cptkip.task.basic_runner as runner

# Run the loop for 1 seconds
finish = time.monotonic() + 1


def task() -> bool:
    return time.monotonic() < finish


runner.run([task])
```

| `cptkip/task/basic_runner` |                   |
|----------------------------|-------------------|
| Ram at Start               | Used: 928 bytes   |
| RAM at Finish before GC    | Used: 8,176 bytes |
| RAM at Finish after GC     | Used: 3,168 bytes |

## `cptkip/task/basic_runner_async.py`

Code under test:

```python
import asyncio

import cptkip.task.basic_runner_async as runner


async def task() -> None:
    await asyncio.sleep(0.1)


runner.run([task])
```

| `cptkip/task/basic_runner_async` |                    |
|----------------------------------|--------------------|
| Ram at Start                     | Used: 944 bytes    |
| RAM at Finish before GC          | Used: 12,560 bytes |
| RAM at Finish after GC           | Used: 11,840 bytes |

## `cptkip/task/periodic_task.py`

Code under test:

```python
import time
import cptkip.task.basic_runner as runner
import cptkip.task.periodic_task as periodic_task

finish = time.monotonic() + 1


def should_continue() -> bool:
    return time.monotonic() < finish


def one() -> None:
    pass


task_one = periodic_task.create(one, frequency=3, continue_func=should_continue)

runner.run([task_one])
```

| `cptkip/task/periodic_task` |                   |
|-----------------------------|-------------------|
| Ram at Start                | Used: 1,136 bytes |
| RAM at Finish before GC     | Used: 7,888 bytes |
| RAM at Finish after GC      | Used: 4,816 bytes |

## `cptkip/task/periodic_task_async.py`

Code under test:

```python
import time, asyncio
import cptkip.task.basic_runner_async as runner
import cptkip.task.periodic_task_async as periodic_task

finish = time.monotonic() + 1


def should_continue() -> bool:
    return time.monotonic() < finish


async def one() -> None:
    await asyncio.sleep(0.1)


task_one = periodic_task.create(one, frequency=3, continue_func=should_continue)

runner.run([task_one])
```

| `cptkip/task/periodic_task_async` |                    |
|-----------------------------------|--------------------|
| Ram at Start                      | Used: 1,184 bytes  |
| RAM at Finish before GC           | Used: 16,368 bytes |
| RAM at Finish after GC            | Used: 14,144 bytes |

## `cptkip/hal/digitalpin.py`

Code under test:

```python
import cptkip.config.configuration as config
import cptkip.pin.output_pin as pin

led = pin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)
led.value = True
led.value = False
```

| `cptkip/hal/digitalpin.py` |                   |
|----------------------------|-------------------|
| Ram at Start               | Used: 912 bytes   |
| RAM at Finish before GC    | Used: 6,064 bytes |
| RAM at Finish after GC     | Used: 6,064 bytes |

## `cptkip/hal/pwmpin.py`

Code under test:

```python
import cptkip.config.configuration as config
import cptkip.pin.pwm_pin as pin

led = pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
led.value = 0.8
led.value = 0.2
led.off()
```

| `cptkip/hal/pwmpin.py`  |                   |
|-------------------------|-------------------|
| Ram at Start            | Used: 928 bytes   |
| RAM at Finish before GC | Used: 6,128 bytes |
| RAM at Finish after GC  | Used: 6,128 bytes |

## `cptkip/hal/pixels.py`

Code under test:

```python
import time

import cptkip.config.configuration as config
import cptkip.device.pixels as pixel

pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)

finish = time.monotonic() + 2
r = 10
rdx = 10
while time.monotonic() < finish:
    r += rdx
    if r > 240:
        rdx = -10
    if r < 20:
        rdx = 10
    pixels.fill((r, 0, 0))
    pixels.write()
    time.sleep(0.05)

pixels.fill(pixel.OFF)
pixels.write()
```

| `cptkip/hal/pixels.py`  |                   |
|-------------------------|-------------------|
| Ram at Start            | Used: 1,040 bytes |
| RAM at Finish before GC | Used: 9,024 bytes |
| RAM at Finish after GC  | Used: 7,744 bytes |

## `animation/rainbow`

Code under test:

```python
import time
from adafruit_led_animation.animation.rainbow import Rainbow

import cptkip.config.configuration as config
import cptkip.device.pixels as pixel

pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)
animation = Rainbow(pixels, speed=0.1, period=2)
animation.animate()

finish = time.monotonic() + 2
while time.monotonic() < finish:
    animation.animate()

animation.freeze()
pixels.fill(pixel.OFF)
pixels.write()
```

| `animation/rainbow.py`  |                    |
|-------------------------|--------------------|
| Ram at Start            | Used: 1,152 bytes  |
| RAM at Finish before GC | Used: 25,888 bytes |
| RAM at Finish after GC  | Used: 15,872 bytes |

## `cptkip/device/button.py`

Code under test:

```python
import time

import cptkip.config.configuration as config
from cptkip.device.button import Button
import cptkip.pin.input_pin as inputpin


def single_click_handler() -> None:
    print('Single click!')


input_pin = inputpin.InputPin(config.BUTTON_PIN)

button = Button(input_pin, click=single_click_handler)

finish = time.monotonic() + 2
while time.monotonic() < finish:
    button.update()
```

| `cptkip/device/button.py` |                    |
|---------------------------|--------------------|
| Ram at Start              | Used: 1,168 bytes  |
| RAM at Finish before GC   | Used: 11,968 bytes |
| RAM at Finish after GC    | Used: 11,920 bytes |

## `cptkip/device/led.py`

Code under test:

```python
import time

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.color import JADE

import cptkip.config.configuration as config
import cptkip.device.led as device
import cptkip.pin.pwm_pin as pin

pin = pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
led = device.Led(pin)
animation = Blink(led, speed=0.5, color=JADE)

finish = time.monotonic() + 2
while time.monotonic() < finish:
    animation.animate()

animation.freeze()
led.off()
```

| `cptkip/device/led.py`  |                    |
|-------------------------|--------------------|
| Ram at Start            | Used: 1,568 bytes  |
| RAM at Finish before GC | Used: 20,816 bytes |
| RAM at Finish after GC  | Used: 14,896 bytes |

## `cptkip/device/melody.py`

Code under test:

```python
import time

import cptkip.config.configuration as config
import cptkip.device.melody as melody
import cptkip.pin.buzzer_pin as buzzerpin

pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
pin.volume = 0.1

scale = [
    "C4:1", "D:1", "E:1", "F:1", "G:1", "A:1", "B:1", "C5:1",
    "B4:1", "A:1", "G:1", "F:1", "E:1", "D:1", "C:1"]

jingle_bells = [
    "E4:2", "E:2", "E:4", "E:2", "E:2", "E:4",
    "E:2", "G:2", "C:2", "D:2", "E:8",
    "F:2", "F:2", "F:2", "F:2", "F:2", "E:2", "E:2", "E:1", "E:1",
    "E:2", "D:2", "D:2", "E:2", "D:4", "G:2", "R:2",
    "E:2", "E:2", "E:4", "E:2", "E:2", "E:4",
    "E:2", "G:2", "C:2", "D:2", "E:8",
    "F:2", "F:2", "F:2", "F:2", "F:2", "E:2", "E:2", "E:1", "E:1",
    "G:2", "G:2", "F:2", "D:2", "C:8",
    "R:8"]

melody_sequence = melody.MelodySequence(
    melody.Melody(pin, melody.decode_melody(scale), 0.2),
    melody.Melody(pin, melody.decode_melody(jingle_bells), 0.1))

finish = time.monotonic() + 2

while time.monotonic() < finish:
    melody_sequence.play()

pin.off()

```

| `cptkip/device/led.py`  |                    |
|-------------------------|--------------------|
| Ram at Start            | Used: 1,760 bytes  |
| RAM at Finish before GC | Used: 17,216 bytes |
| RAM at Finish after GC  | Used: 13,120 bytes |

## Experiments with the old framework

Some tests were run using the old runner framework which is a bit memory hungry to see how much it can potentially be
optimised.

Using the original logging framework.

| Example                                                                        | Ram at Start                            | RAM at Finish before GC                 | RAM at Finish after GC                  |
|--------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| `cptkip.task.basic_runner.py`                                                  | Used: 28,416 bytes, Free: 139,264 bytes | Used: 61,600 bytes, Free: 106,080 bytes | Used: 32,208 bytes, Free: 135,472 bytes |
| `cptkip.task.basic_runner.py` with unrequired code removed from `scheduler.py` | Used: 25,664 bytes, Free: 142,016 bytes | Used: 43,296 bytes, Free: 124,384 bytes | Used: 27,552 bytes, Free: 140,128 bytes |
| `cptkip.task.basic_runner.py` with unrequired code moved to `triggerable.py`   | Used: 25,680 bytes, Free: 142,000 bytes | Used: 43,264 bytes, Free: 124,416 bytes | Used: 27,568 bytes, Free: 140,112 bytes |
| `manual_runner.py`                                                             | Used: 24,672 bytes, Free: 142,112 bytes | Used: 29,536 bytes, Free: 137,248 bytes | Used: 27,872 bytes, Free: 138,912 bytes |

Using the memory optimised logging framework.

| Example                                                                      | Ram at Start                            | RAM at Finish before GC                 | RAM at Finish after GC                  |
|------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| `cptkip.task.basic_runner.py` with unrequired code moved to `triggerable.py` | Used: 18,336 bytes, Free: 149,344 bytes | Used: 38,896 bytes, Free: 128,784 bytes | Used: 20,224 bytes, Free: 147,456 bytes |
| `manual_runner.py`                                                           | Used: 17,552 bytes, Free: 149,232 bytes | Used: 24,256 bytes, Free: 142,528 bytes | Used: 20,816 bytes, Free: 145,968 bytes |

## Lessons learned

* Prefer small module with only a few items of functionality over larger modules to save RAM.
* F strings are expensive in temporary memory usage, it's more efficient to use `print()` with
  multiple arguments.

## Notes

* Logging is expensive when using `adadfruit_logging` so the built-in logging package as part of `cptkip.core`
  has been simplified to remove all dependencies to use far less RAM. If more complex logging is required then
  use the `cptkip.logging` package which has an identical interface but uses the full logging frameworks.
* The asyncio library is also expensive for memory, adding around 10Kb to the usage.