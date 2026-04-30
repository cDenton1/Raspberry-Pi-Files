from machine import Pin
import time

clk = Pin(15, Pin.IN, Pin.PULL_UP)
dt  = Pin(14, Pin.IN, Pin.PULL_UP)
sw  = Pin(13, Pin.IN, Pin.PULL_UP)

last_clk = clk.value()

def rotation():
    global last_clk

    current = clk.value()
    delta = 0

    if last_clk == 1 and current == 0:
        if dt.value() == 1:
            delta = 1     # clockwise
        else:
            delta = -1    # counterclockwise

    last_clk = current
    return delta

def button():
    if sw.value() == 0:  # pressed
        time.sleep(0.3)  # debounce
        return(True)
    return(False)

