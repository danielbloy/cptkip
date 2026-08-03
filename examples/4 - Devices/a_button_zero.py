#
# This example demonstrates using a Button to blink the board LED.
# Uses `cptkip.zero.button`.
#
import time

import cptkip.core.logging as log
from cptkip.zero.button import create_button
from cptkip.zero.led import create_led

log.set_log_level(log.INFO)

led = create_led()


def switch():
    if led.brightness > 0:
        led.brightness = 1
    else:
        led.brightness = 0


def single_click_handler() -> None:
    log.info('Single click!')
    switch()


def multi_click_handler() -> None:
    log.info('Multi click!')
    switch()
    time.sleep(0.25)
    switch()


def long_press_handler() -> None:
    log.info('Long press!')


button = create_button(
    click=single_click_handler,
    multi_click=multi_click_handler,
    long_click=long_press_handler)

# Run the loop for 10 seconds
log.info("Press the button to change the LED.")
finish = time.monotonic() + 10

while time.monotonic() < finish:
    button.update()
