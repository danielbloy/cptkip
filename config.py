import cptkip.core.environment as environment
from cptkip.core.logging import ERROR

LOG_LEVEL = ERROR

TEST_VALUE = 123.456

TEST_STRING = "Hello world!"

DEBUG = True

LED_PIN = None
if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    # Support using the LED pin from either a plain old Pi Pico board or a Pimoroni Tiny board.
    try:
        LED_PIN = board.LED
        print('Using LED')
    except AttributeError:
        try:
            LED_PIN = board.LED_G
            print('Using LED_G')
        except AttributeError:
            pass

if not LED_PIN:
    print('No LED found')
