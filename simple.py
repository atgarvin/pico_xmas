from machine import Pin
from time import sleep_ms


#========================
# INITIALIZE LIGHT PINS
#========================

# The names chosen (R1, R2, etc) are arbitrary and can (and should) be renamed.
# Name your lights something that makes sense and can easily be identified later.
# Examples:
#   LAWN, TREE, ROOF, etc
#
# The Pin assignments can be any GPIO pin that is free on the raspberry pi.
# For simplicity, 0-3 have been chosen for this script.
# Only 4 are used here, but you can add (or subtract) as many as you need.
R1 = Pin(0, Pin.OUT)
R2 = Pin(1, Pin.OUT)
R3 = Pin(2, Pin.OUT)
G1 = Pin(3, Pin.OUT)


#========================
# MUSIC
#========================

# Music timing
BPM = 120.0             # Set the BPM to match your chosen song
BPS = BPM/60.0          # Ignore this - it is set automatically
QTR_ms = int(1000/BPS)  # Ignore this - it is set automatically

# Music commands
# This is what dictates the sequence of turning lights on/off.
# You can add as many commands as you like.
# You can also add a comment to each section of the music to make it easier to look at.
#   - examples given below
#   - comments are started with a # and are ignored by the script.
# Add as much blank space as you like as well.
#
# Each command is a dictionary with 3 keys.
#   - "on": list of lights to turn on
#       - (you don't need to specify lights that are already on, but you can if that helps)
#   - "off": list of lights to turn off
#       - (you don't need to specify lights that are already off, but you can if that helps)
#   - "qtr": the number of quarter notes (beats) to display the command for
#       - (how long to leave the lights in this state before moving to the next command)
#       - it's okay to use any number bigger/smaller than 1.
#           For example, 0.25 is 1/4 of a quarter note (in other words, a 16th note)
#           Similarly, a value of 4 quarter notes is (likely) a full measure (in 4/4 time).
commands = [
    # intro
    {"on": [R1], "off": [], "qtr": 1},
    {"on": [R2], "off": [], "qtr": 1},
    {"on": [R3], "off": [], "qtr": 1},
    {"on": [G1], "off": [], "qtr": 1},
    {"on": [], "off": [R1], "qtr": 1},
    {"on": [], "off": [R2], "qtr": 1},
    {"on": [], "off": [R3], "qtr": 1},
    {"on": [], "off": [G1], "qtr": 1},
    # verse
    {"on": [R1], "off": [], "qtr": 0.5},
    {"on": [R2], "off": [], "qtr": 0.5},
    {"on": [R3], "off": [], "qtr": 0.5},
    {"on": [G1], "off": [], "qtr": 0.5},
    {"on": [], "off": [R1], "qtr": 0.5},
    {"on": [], "off": [R2], "qtr": 0.5},
    {"on": [], "off": [R3], "qtr": 0.5},
    {"on": [], "off": [G1], "qtr": 0.5},
    # chorus
    {"on": [R1, R2, R3, G1], "off": [], "qtr": 1},
    {"on": [], "off": [R1, R2, R3, G1], "qtr": 1},
    {"on": [R1, R2, R3, G1], "off": [], "qtr": 1},
    {"on": [], "off": [R1, R2, R3, G1], "qtr": 1}
]

#========================
# LED CONTROL FUNCTIONS
#========================
def update_leds(turn_on = [], turn_off = []):
    for led in turn_on:
        led.on()
    for led in turn_off:
        led.off()


def all_on():
    update_leds([R1, R2, R3, G1], [])


def all_off():
    update_leds([], [R1, R2, R3, G1])


def playback(commands=[]):
    for cmd in commands:
        update_leds(cmd["on"], cmd["off"])
        sleep_ms(int(cmd["qtr"]*QTR_ms))


def playback_test(iterations=1):
    for i in range(0, iterations):
        playback(commands)


if __name__ == "__main__":
    # Play 10 times and then stop
    playback_test(10)

    # Alternatively, play indefinitely by uncommenting these 2 lines:
    #while True:
    #    playback_test()

