import board

TOP_LEFT_LED_PIN = board.IO5
TOP_CENTRE_LED_PIN = board.IO8
TOP_RIGHT_LED_PIN = board.RX

MIDDLE_LEFT_LED_PIN = board.IO6
MIDDLE_CENTRE_LED_PIN = board.TX
MIDDLE_RIGHT_LED_PIN = board.IO9

BOTTOM_LEFT_LED_PIN = board.IO2
BOTTOM_CENTRE_LED_PIN = board.IO0
BOTTOM_RIGHT_LED_PIN = board.IO1

BUZZER_PIN = board.IO4

LED_PINS = [
    TOP_LEFT_LED_PIN, TOP_CENTRE_LED_PIN, TOP_RIGHT_LED_PIN,
    MIDDLE_LEFT_LED_PIN, MIDDLE_CENTRE_LED_PIN, MIDDLE_RIGHT_LED_PIN,
    BOTTOM_LEFT_LED_PIN, BOTTOM_CENTRE_LED_PIN, BOTTOM_RIGHT_LED_PIN
]

TL = 0
TC = 1
TR = 2
ML = 3
MC = 4
MR = 5
BL = 6
BC = 7
BR = 9

scale = '''C4:1 D:1 E:1 F:1 G:1 A:1 B:1 C5:1
           B4:1 A:1 G:1 F:1 E:1 D:1 C:1'''

jingle_bells = [
    "E4:2", "E:2", "E:4", "E:2", "E:2", "E:4",
    "E:2", "G:2", "C:2", "D:2", "E:8",
    "F:2", "F:2", "F:2", "F:2", "F:2", "E:2", "E:2", "E:1", "E:1",
    "E:2", "D:2", "D:2", "E:2", "D:4", "G:2", "R:2",
    "E:2", "E:2", "E:4", "E:2", "E:2", "E:4",
    "E:2", "G:2", "C:2", "D:2", "E:8",
    "F:2", "F:2", "F:2", "F:2", "F:2", "E:2", "E:2", "E:1", "E:1",
    "G:2", "G:2", "F:2", "D:2", "C:8",
    "R:8"]
