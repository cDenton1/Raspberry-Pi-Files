from machine import Pin

# GPIO pins for each LED - listed backwards to go left to right
led_pins = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2] 

# initialize LEDs
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

def bar_clear():
    for led in leds:
        led.value(0)
        
def show_queue(queue):
    bar_clear()
    # queue = queue[:len(leds)]
    start = len(leds) - len(queue)
    for i in range(len(queue)):
        leds[start + i].value(1)
