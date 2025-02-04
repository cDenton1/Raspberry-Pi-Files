import machine
import time
import random

# Set up LEDs and buttons
led_pins = [machine.Pin(12, machine.Pin.OUT),  # red LED
            machine.Pin(11, machine.Pin.OUT),  # blue LED
            machine.Pin(10, machine.Pin.OUT)]  # green LED

button_pins = [machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP),  # red LED button
               machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP),  # green LED button
               machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)]  # blue LED button

# Game variables
sequence = []
player_input = []
game_over = False
level = 1

def flash_leds():
    for index in sequence:
        led_pins[index].on()
        time.sleep(0.5)
        led_pins[index].off()
        time.sleep(0.2)

def get_player_input():
    player_input.clear()
    print("Press buttons in sequence:")
    while len(player_input) < len(sequence):
        for i in range(3):  # check for each button
            if not button_pins[i].value():  # button pressed
                player_input.append(i)
                led_pins[i].on()  # light up the corresponding LED
                # print(f"Button {i} pressed")  # debugging
                time.sleep(0.3)  # debounce delay
                led_pins[i].off()  # turn off the LED after a short time
                while not button_pins[i].value():  # wait until the button is released
                    time.sleep(0.05)  # small delay to avoid too many checks
    return player_input

def check_player_input():
    if player_input == sequence:
        return True
    return False

def add_to_sequence():
    sequence.append(random.randint(0, 2))

def reset_game():
    global sequence, level
    sequence = []
    level = 1
    time.sleep(1)

# main game loop
while True:
    if game_over:
        reset_game()
        game_over = False
    
    print(f"Level {level}")
    
    # add a new LED to the sequence
    add_to_sequence()
    
    # flash the LEDs in the sequence
    flash_leds()
    
    # get player's input
    player_input = get_player_input()
    
    # check if the player succeeded or failed
    if check_player_input():
        print("Correct!")
        level += 1
    else:
        print("Wrong! Game Over!")
        i = 0
        while i < 3:
            for j in range(3):
                led_pins[j].on()
                time.sleep(0.2)
                led_pins[j].off()
            i += 1
        game_over = True

    time.sleep(1)
