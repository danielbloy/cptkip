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
| RAM at Finish before GC    | Used: 6,352 bytes |
| RAM at Finish after GC     | Used: 6,352 bytes |

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
| RAM at Finish before GC | Used: 5,744 bytes |
| RAM at Finish after GC  | Used: 5,744 bytes |

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
| RAM at Finish before GC | Used: 8656 bytes  |
| RAM at Finish after GC  | Used: 7,376 bytes |

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
| RAM at Finish before GC | Used: 16,992 bytes |
| RAM at Finish after GC  | Used: 16,000 bytes |

## `cptkip/device/button.py`

Code under test:

```python
import time

import cptkip.config.configuration as config
from cptkip.device.button import Button
import cptkip.pin.input_pin as inputpin


def single_click_handler() -> None:
    print('Single click!')


input_pin = inputpin.InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

button = Button(input_pin, click=single_click_handler)

finish = time.monotonic() + 2
while time.monotonic() < finish:
    button.update()
```

| `cptkip/device/button.py` |                    |
|---------------------------|--------------------|
| Ram at Start              | Used: 1,168 bytes  |
| RAM at Finish before GC   | Used: 11,824 bytes |
| RAM at Finish after GC    | Used: 11,776 bytes |

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
| RAM at Finish before GC | Used: 24,032 bytes |
| RAM at Finish after GC  | Used: 14,976 bytes |

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
    melody.Melody(pin, melody.decode_melody(scale), 240),
    melody.Melody(pin, melody.decode_melody(jingle_bells), 480))

finish = time.monotonic() + 2

while time.monotonic() < finish:
    melody_sequence.update()

pin.off()
```

| `cptkip/device/led.py`  |                    |
|-------------------------|--------------------|
| Ram at Start            | Used: 1,744 bytes  |
| RAM at Finish before GC | Used: 44,064 bytes |
| RAM at Finish after GC  | Used: 13,440 bytes |
