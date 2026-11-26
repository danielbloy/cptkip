import cptkip.core.environment as environment

if environment.are_pins_available():
    import board

    TOP_LEFT_LED_PIN = board.IO5
    TOP_CENTRE_LED_PIN = board.IO8
    TOP_RIGHT_LED_PIN = board.RX

    MIDDLE_LEFT_LED_PIN = board.IO6
    MIDDLE_CENTRE_LED_PIN = board.TX
    MIDDLE_RIGHT_LED_PIN = board.IO10

    BOTTOM_LEFT_LED_PIN = board.IO2
    BOTTOM_CENTRE_LED_PIN = board.IO0
    BOTTOM_RIGHT_LED_PIN = board.IO1

    BUZZER_PIN = board.IO4
