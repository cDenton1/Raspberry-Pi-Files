import time
import random
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C     # SSD1306 OLED library

WIDTH = 128    # OLED display width
HEIGHT = 64    # OLED display height

i2c = I2C(0, scl=Pin(5), sda=Pin(4))     # initialize I2C
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)   # initialize OLED

button_heads = Pin(14, Pin.IN, Pin.PULL_UP)  # button for heads
button_tails = Pin(15, Pin.IN, Pin.PULL_UP)  # button for tails

# draw an ellipse to simulate a rotating circle
def draw_ellipse(cx, cy, rx, ry, fill=1):
    if ry == 0:     # Prevent division by zero
        return
    for x in range(-rx, rx + 1):
        for y in range(-ry, ry + 1):
            if (x**2) / (rx**2) + (y**2) / (ry**2) <= 1:
                oled.pixel(cx + x, cy + y, fill)

# draw the coin with text
def draw_coin(text, rx, ry):
    oled.fill(0)     # clear display
    draw_ellipse(64, 32, rx, ry, fill=1)             # draw an ellipse to represent the coin
    draw_ellipse(64, 32, rx - 2, ry - 2, fill=0)     # outline by clearing the inner ellipse
    if ry > 5:             # display text only if the coin is "wide enough" during the flip
        x_pos = 64 - 3     # center H or T
        y_pos = 28
        oled.text(text, x_pos, y_pos, 1)
    oled.show()

# coin flip animation
def coin_flip_animation():
    result = random.choice(["H", "T"])     # final result

    # simulate flipping by changing the ellipse height (ry)
    for _ in range(3):                     # repeat flipping cycles
        for ry in range(20, 2, -2):        # flatten the ellipse
            draw_coin("", 20, ry)
            time.sleep(0.005) 
        for ry in range(2, 21, 2):         # expand the ellipse
            draw_coin("", 20, ry)
            time.sleep(0.005) 

    # final state: Show the result
    oled.fill(0)     # clear display
    draw_ellipse(64, 32, 20, 20, fill=1)     # draw the final circle
    draw_ellipse(64, 32, 18, 18, fill=0)     # outline
    oled.text(result, 60, 28, 1)             # center the result ("H" or "T")
    oled.show()
    time.sleep(0.5)     # show the result

    return result

# main game function
def game():
    oled.fill(0)
    oled.text("Left for Tails", 10, 25) 
    oled.text("Right for Heads", 6, 45)
    oled.show()

    # wait for the user to press a button
    while True:
        if not button_heads.value():     # check if heads button is pressed
            oled.fill(0)
            oled.text("You chose Heads", 5, 10)
            oled.show()
            time.sleep(1)
            user_guess = "H"
            break
        elif not button_tails.value():     # check if tails button is pressed
            oled.fill(0)
            oled.text("You chose Tails", 5, 10)
            oled.show()
            time.sleep(1)
            user_guess = "T"
            break

    result = coin_flip_animation()     # flip the coin and get the result

    # check if the user won
    oled.fill(0)
    if user_guess == result:
        oled.text("You win!", 27, 10)
    else:
        oled.text("You lose!", 27, 10)
    oled.show()
    time.sleep(2)     # show the result
    oled.fill(0)
    oled.show()       # clear the screen

game()   # run the game
