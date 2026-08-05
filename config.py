import cptkip.core.environment as environment
from cptkip.core.logging import INFO

LOG_LEVEL = INFO

TEST_VALUE = 123.456

TEST_STRING = "Hello world!"

DEBUG = True

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

################################################################################
# L E D
################################################################################
LED_PIN = None
LED_INVERT = False
if environment.are_pins_available():
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
PIXELS_COUNT = 8

if environment.are_pins_available():
    # noinspection PyUnresolvedReferences
    PIXELS_PIN = board.GP28

if not PIXELS_PIN:
    print('No NeoPixels found')

################################################################################
# B U Z Z E R
################################################################################
BUZZER_PIN = None

if environment.are_pins_available():
    # noinspection PyUnresolvedReferences
    BUZZER_PIN = board.GP3

if not BUZZER_PIN:
    print('No Buzzer found')

################################################################################
# I 2 S    A U D I O
################################################################################
I2S_BIT_CLOCK = None
I2S_LEFT_RIGHT_CLOCK = None
I2S_DATA = None

if environment.are_pins_available():
    # noinspection unresolved-references
    I2S_BIT_CLOCK = board.GP0
    # noinspection unresolved-references
    I2S_LEFT_RIGHT_CLOCK = board.GP1
    # noinspection unresolved-references
    I2S_DATA = board.GP2

if not I2S_BIT_CLOCK or not I2S_LEFT_RIGHT_CLOCK or not I2S_DATA:
    print('No I2S Audio found')
