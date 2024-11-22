from machine import Pin
from time import sleep_ms


R1 = Pin(0, Pin.OUT)
R2 = Pin(1, Pin.OUT)
R3 = Pin(2, Pin.OUT)
G1 = Pin(3, Pin.OUT)

# music timing
BPM = 120
BPS = BPM/60
QTR_ms = int(1000/BPS)


def update_leds(turn_on = [], turn_off = []):
    for led in turn_on:
        led.value(1)
    for led in turn_off:
        led.value(0)

def all_on():
    update_leds([R1, R2, R3, G1], [])

def all_off():
    update_leds([], [R1, R2, R3, G1])


def sleep_test(bpm):
    bps = bpm/60
    qtr = int(1000/bps)

    for i in range(0,4):
        R1.value(1)
        sleep_ms(qtr)
        R2.value(1)
        sleep_ms(qtr)
        R3.value(1)
        sleep_ms(qtr)
        G1.value(1)
        sleep_ms(qtr)

        R1.value(0)
        sleep_ms(qtr)
        R2.value(0)
        sleep_ms(qtr)
        R3.value(0)
        sleep_ms(qtr)
        G1.value(0)
        sleep_ms(qtr)

def playback(commands=[]):
    for cmd in commands:
        update_leds(cmd["on"], cmd["off"])
        sleep_ms(int(cmd["qtr"]*QTR_ms))

def playback_test(iterations=1):
    commands = [
        {"on": [R1], "off": [], "qtr": 1},
        {"on": [R2], "off": [], "qtr": 1},
        {"on": [R3], "off": [], "qtr": 1},
        {"on": [G1], "off": [], "qtr": 1},
        {"on": [], "off": [R1], "qtr": 1},
        {"on": [], "off": [R2], "qtr": 1},
        {"on": [], "off": [R3], "qtr": 1},
        {"on": [], "off": [G1], "qtr": 1},
        {"on": [R1], "off": [], "qtr": 0.5},
        {"on": [R2], "off": [], "qtr": 0.5},
        {"on": [R3], "off": [], "qtr": 0.5},
        {"on": [G1], "off": [], "qtr": 0.5},
        {"on": [], "off": [R1], "qtr": 0.5},
        {"on": [], "off": [R2], "qtr": 0.5},
        {"on": [], "off": [R3], "qtr": 0.5},
        {"on": [], "off": [G1], "qtr": 0.5},
        {"on": [R1, R2, R3, G1], "off": [], "qtr": 1},
        {"on": [], "off": [R1, R2, R3, G1], "qtr": 1},
        {"on": [R1, R2, R3, G1], "off": [], "qtr": 1},
        {"on": [], "off": [R1, R2, R3, G1], "qtr": 1}
    ]
    for i in range(0, iterations):
        playback(commands)


if __name__ == "__main__":
    playback_test(10)

