from machine import Pin
from time import sleep_ms, ticks_ms


#===================
# INITIALIZE PINS
#===================

# 1. SETTING UP THE LIGHTS
#
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


# 2. SETTING UP BUTTONS
#
# Optionally, you can control the lights to some extent with buttons.
# Two buttons are in use for this script:
#   One for starting/restarting the show.
#   One for ending the show and turning all the lights on.
#Buttons for controlling the state_idle
button_1 = Pin(17, Pin.IN, Pin.PULL_UP)
previous_ticks_1 = ticks_ms()
debounce_time_1 = 200

button_2 = Pin(16, Pin.IN, Pin.PULL_UP)
previous_ticks_2 = ticks_ms()
debounce_time_2 = 200


#===================
# OTHER VARIABLES
#===================

# States
state_on = 0
state_play = 1
state_idle = 2
current_state = state_play  # Start playing immediately when powered on.
                            # Change this to start in a different state.

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
def update_leds(on=[], off=[]):
    for led in on:
        led.on()
    for led in off:
        led.off()


def all_on():
    update_leds([R1, R2, R3, G1], [])


def all_off():
    update_leds([], [R1, R2, R3, G1])


#========================
# BUTTON INTERRUPTS
#========================
def button_1_pressed(button):
    global current_state
    global previous_ticks_1
    global debounce_time_1
    current_ticks = ticks_ms()
    if current_ticks - previous_ticks_1 > debounce_time_1:
        previous_ticks_1 = current_ticks
        #R1.toggle()
        current_state = state_play


def button_2_pressed(button):
    global current_state
    global previous_ticks_2
    global debounce_time_2
    current_ticks = ticks_ms()
    if current_ticks - previous_ticks_2 > debounce_time_2:
        previous_ticks_2 = current_ticks
        #G1.toggle()
        current_state = state_on


#========================
# STATES
#========================
def state_playback():
    for cmd in commands:
        if current_state != state_idle:
            break
        update_leds(cmd["on"], cmd["off"])
        sleep_ms(int(cmd["qtr"]*QTR_ms))


#========================
# ENTRYPOINT
#========================


if __name__ == "__main__":
    global current_state

    # setup interrupts
    button_1.irq(trigger=Pin.IRQ_RISING, handler=button_1_pressed)
    button_2.irq(trigger=Pin.IRQ_RISING, handler=button_2_pressed)

    # main loop
    while True:
        if current_state == state_play:
            all_off()
            current_state = state_idle
            while current_state == state_idle:
                state_playback()
        elif current_state == state_on:
            all_on()
            while current_state == state_on:
                pass
        # Add more states here as needed
        #elif current_state == some_other_state:
        #    # your code here
        #    pass


