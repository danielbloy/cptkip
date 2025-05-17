import asyncio
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.device.button as button
import cptkip.pin.inputpin as inputpin
import cptkip.pin.outputpin as outputpin
import cptkip.task.basic_runner as runner

memory.report_memory_usage()

log.set_log_level(log.INFO)

led = outputpin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)


async def single_click_handler() -> None:
    log.info('Single click!')
    led.value = not led.value


async def multi_click_handler() -> None:
    log.info('Multi click!')
    led.value = not led.value
    await asyncio.sleep(0.25)
    led.value = not led.value


async def long_press_handler() -> None:
    log.info('Long press!')


# Run the loop for 10 seconds
log.info("Press the button to change the LED.")
finish = time.monotonic() + 10


# Should we continue to run or not?
def should_continue() -> bool:
    return time.monotonic() < finish


# Executed once at the beginning and before any initial delay.
async def begin() -> None:
    log.info(f"{time.monotonic()}: BEGIN")


# Executed once at the end.
async def end() -> None:
    log.info(f"{time.monotonic()}: END")
    led.off()


task = button.create(
    inputpin.InputPin(config.BUTTON_PIN),
    click=single_click_handler,
    multi_click=multi_click_handler,
    long_click=long_press_handler,
    continue_func=should_continue,
    begin=begin,
    end=end)

runner.run([task])

memory.report_memory_usage_and_free()
