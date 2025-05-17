import cptkip.core.environment as environment
from cptkip.core.logging import ERROR

LOG_LEVEL = ERROR

TEST_VALUE = 123.456

TEST_STRING = "Hello world!"

DEBUG = True

################################################################################
# L E D
################################################################################
LED_PIN = None
LED_INVERT = False
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
            LED_INVERT = True
            print('Using LED_G')
        except AttributeError:
            pass

if not LED_PIN:
    print('No LED found')

################################################################################
# B U T T O N
################################################################################
BUTTON_PIN = None
BUTTON_INVERT = False
if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    # Support using the button from a Pimoroni Tiny board.
    try:
        BUTTON_PIN = board.BUTTON
        print('Using BUTTON')
    except AttributeError:
        try:
            BUTTON_PIN = board.GP27
            print('Using GP27')
        except AttributeError:
            pass

if not BUTTON_PIN:
    print('No Button found')

################################################################################
# N E O P I X E L S
################################################################################
PIXELS_PIN = None

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    PIXELS_PIN = board.GP28

if not PIXELS_PIN:
    print('No NeoPixels found')

################################################################################
# B U Z Z E R
################################################################################
BUZZER_PIN = board.GP2
