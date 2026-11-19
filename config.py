import cptkip.core.environment as environment
from cptkip.core.logging import INFO

DEBUG = True

################################################################################
# T E S T    V A L U E S
################################################################################
TEST_VALUE = 123.456

TEST_STRING = "Hello world!"

################################################################################
# L O G G I N G
################################################################################
LOG_LEVEL = INFO

################################################################################
# L E D
################################################################################
LED_PIN = None
LED_INVERT = False

################################################################################
# B U T T O N
################################################################################
BUTTON_PIN = None
BUTTON_PULLUP = True

################################################################################
# B U Z Z E R
################################################################################
BUZZER_PIN = None

################################################################################
# N E O P I X E L S
################################################################################
PIXELS_PIN = None
PIXELS_COUNT = 8

################################################################################
# I 2 S    A U D I O
################################################################################
I2S_BIT_CLOCK = None
I2S_LEFT_RIGHT_CLOCK = None
I2S_DATA = None

################################################################################
# D E V I C E    S P E C I F I C    S E T T I N G S
################################################################################

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board
    import sys

    # The platform will help us determine which pins to use.
    pico: bool = sys.platform.lower() == "rp2040" or sys.platform.lower() == "rp2350"
    espressif: bool = sys.platform.lower() == "espressif"

    ################################################################################
    # L E D
    ################################################################################
    # Support using the LED pin from either a plain old Pi Pico board or a Pimoroni Tiny board.
    try:
        # noinspection PyUnresolvedReferences
        LED_PIN = board.LED
    except AttributeError:
        try:
            # noinspection PyUnresolvedReferences
            LED_PIN = board.LED_G
            LED_INVERT = True
        except AttributeError:
            pass

    ################################################################################
    # B U T T O N
    ################################################################################
    # Support using the button from a Pimoroni Tiny or ESP-32 board.
    try:
        # noinspection PyUnresolvedReferences
        BUTTON_PIN = board.BUTTON
        BUTTON_PULLUP = None
    except AttributeError:
        try:
            if pico:
                # noinspection PyUnresolvedReferences
                BUTTON_PIN = board.GP27

            if espressif:
                # noinspection PyUnresolvedReferences
                BUTTON_PIN = board.IO0

        except AttributeError:
            pass

    ################################################################################
    # B U Z Z E R
    ################################################################################
    try:
        if pico:
            # noinspection PyUnresolvedReferences
            BUZZER_PIN = board.GP3

        if espressif:
            # noinspection PyUnresolvedReferences
            BUZZER_PIN = board.IO1

    except AttributeError:
        pass

    ################################################################################
    # N E O P I X E L S
    ################################################################################
    # Support the onboard NeoPixel from an ESP-32 board.
    try:
        # noinspection PyUnresolvedReferences
        PIXELS_PIN = board.NEOPIXEL
    except AttributeError:
        try:
            if pico:
                # noinspection PyUnresolvedReferences
                PIXELS_PIN = board.GP28

            if espressif:
                # noinspection PyUnresolvedReferences
                PIXELS_PIN = board.IO10

        except AttributeError:
            pass

    ################################################################################
    # I 2 S    A U D I O
    ################################################################################
    try:
        if pico:
            # noinspection unresolved-references
            I2S_BIT_CLOCK = board.GP0
            # noinspection unresolved-references
            I2S_LEFT_RIGHT_CLOCK = board.GP1
            # noinspection unresolved-references
            I2S_DATA = board.GP2

        if espressif:
            # noinspection unresolved-references
            I2S_BIT_CLOCK = board.IO3
            # noinspection unresolved-references
            I2S_LEFT_RIGHT_CLOCK = board.IO4
            # noinspection unresolved-references
            I2S_DATA = board.IO5

    except AttributeError:
        pass
