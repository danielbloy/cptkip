#
# This example demonstrates using a Button to blink the board LED.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
from cptkip.device.button import Button
from cptkip.pin.input_pin import InputPin
from cptkip.pin.output_pin import OutputPin

memory.report_memory_usage()

log.set_log_level(log.INFO)

led = OutputPin(config.LED_PIN, invert=config.LED_INVERT)


def single_click_handler() -> None:
    log.info('Single click!')
    led.value = not led.value


def multi_click_handler() -> None:
    log.info('Multi click!')
    led.value = not led.value
    time.sleep(0.25)
    led.value = not led.value


def long_press_handler() -> None:
    log.info('Long press!')


input_pin = InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

button = Button(
    input_pin,
    click=single_click_handler,
    multi_click=multi_click_handler,
    long_click=long_press_handler)

# Run the loop for 10 seconds
log.info("Press the button to change the LED.")
finish = time.monotonic() + 10

while time.monotonic() < finish:
    button.update()

memory.report_memory_usage_and_free()
