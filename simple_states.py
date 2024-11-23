from machine import Pin
from time import sleep_ms, ticks_ms

#===================
# Initialize pins
#===================

# lights
R1 = Pin(0, Pin.OUT)
R2 = Pin(1, Pin.OUT)
R3 = Pin(2, Pin.OUT)
G1 = Pin(3, Pin.OUT)

# music stuff
# (nothing added yet)

# buttons
button_1 = Pin(17, Pin.IN, Pin.PULL_UP)
previous_ticks_1 = ticks_ms()
debounce_time_1 = 200

button_2 = Pin(16, Pin.IN, Pin.PULL_UP)
previous_ticks_2 = ticks_ms()
debounce_time_2 = 200



#===================
# Other stuff
#===================

# states
state_on = 0
state_play = 1
state_idle = 2
current_state = state_play

# music timing
BPM = 120.0
BPS = BPM/60.0
QTR_ms = int(1000/BPS)

# music commands
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


def update_leds(on=[], off=[]):
    for led in on:
        led.on()
    for led in off:
        led.off()


def all_on():
    update_leds([R1, R2, R3, G1], [])


def all_off():
    update_leds([], [R1, R2, R3, G1])


# interrupts
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


def sleep_test(bpm):
    bps = bpm/60
    qtr = int(1000/bps)

    for i in range(0,4):
        R1.on()
        sleep_ms(qtr)
        R2.on()
        sleep_ms(qtr)
        R3.on()
        sleep_ms(qtr)
        G1.on()
        sleep_ms(qtr)

        R1.off()
        sleep_ms(qtr)
        R2.off()
        sleep_ms(qtr)
        R3.off()
        sleep_ms(qtr)
        G1.off()
        sleep_ms(qtr)


def state_playback():
    for cmd in commands:
        if current_state != state_idle:
            break
        update_leds(cmd["on"], cmd["off"])
        sleep_ms(int(cmd["qtr"]*QTR_ms))


def state_test():
    global current_state
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


if __name__ == "__main__":
    # setup interrupts
    button_1.irq(trigger=Pin.IRQ_RISING, handler=button_1_pressed)
    button_2.irq(trigger=Pin.IRQ_RISING, handler=button_2_pressed)

    # run test
    state_test()


