# This is for a Pico 2 W on a test board. We redirect the LED to the green LED
# as the onboard LED does not support PWM.
import board

LED_PIN = board.GP5

BUZZER_PIN = board.GP2  # The Buzzer is also on a different pin
