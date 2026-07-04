import cptkip.core.environment as environment
from cptkip.core.logging import INFO

LOG_LEVEL = INFO

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
        # noinspection PyUnresolvedReferences
        LED_PIN = board.LED
        print('Using LED')
    except AttributeError:
        try:
            # noinspection PyUnresolvedReferences
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
BUTTON_PULLUP = True
if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    # Support using the button from a Pimoroni Tiny board.
    try:
        # noinspection PyUnresolvedReferences
        BUTTON_PIN = board.BUTTON
        BUTTON_PULLUP = None
        print('Using BUTTON')
    except AttributeError:
        try:
            # noinspection PyUnresolvedReferences
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

    # noinspection PyUnresolvedReferences
    PIXELS_PIN = board.GP28

if not PIXELS_PIN:
    print('No NeoPixels found')

################################################################################
# B U Z Z E R
################################################################################
BUZZER_PIN = None

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    # noinspection PyUnresolvedReferences
    BUZZER_PIN = board.GP3

if not BUZZER_PIN:
    print('No Buzzer found')
