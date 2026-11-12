# This is for a Pico-W on a test board. We redirect the LED to the green LED
# as the onboard LED does not support PWM.
import board

LED_PIN = board.GP5
