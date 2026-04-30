from machine import Pin
from time import sleep

# pin mapping
rs = Pin(21, Pin.OUT)
e  = Pin(20, Pin.OUT)
d4 = Pin(19, Pin.OUT)
d5 = Pin(18, Pin.OUT)
d6 = Pin(17, Pin.OUT)
d7 = Pin(16, Pin.OUT)

data_pins = [d4, d5, d6, d7]

def pulse_enable():
    e.value(0)
    sleep(0.001)
    e.value(1)
    sleep(0.001)
    e.value(0)
    sleep(0.001)

def send_nibble(nibble):
    for i in range(4):
        data_pins[i].value((nibble >> i) & 1)
    pulse_enable()

def send_byte(value, mode):
    rs.value(mode)  # 0 = command, 1 = data
    send_nibble(value >> 4)
    send_nibble(value & 0x0F)
    sleep(0.002)

def lcd_command(cmd):
    send_byte(cmd, 0)

def lcd_data(data):
    send_byte(data, 1)

def lcd_init():
    sleep(0.05)

    # Initialize in 4-bit mode
    send_nibble(0x03)
    sleep(0.005)
    send_nibble(0x03)
    sleep(0.001)
    send_nibble(0x03)
    send_nibble(0x02)

    lcd_command(0x28)  # 4-bit, 2 lines
    lcd_command(0x0C)  # Display ON, cursor OFF
    lcd_command(0x06)  # Entry mode
    lcd_command(0x01)  # Clear display
    sleep(0.005)

def lcd_print(text):
    for char in text:
        lcd_data(ord(char))

def lcd_line1():
    lcd_command(0x80) # cursor first line
    
def lcd_line2():
    lcd_command(0xC0) # cursor second line
    
def lcd_clear():
    lcd_command(0x01)

# helper function to make writing on the LCD easier
def lcd_write_line(line_func, text):
    text = text[:16]
    while len(text) < 16:
        text += " "
    line_func()
    lcd_print(text)
