from machine import Pin, ADC, PWM
import utime

# GPIO pins for each LED in the display
led_pins = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# each LED pin as a PWM output to control brightness
pwm_leds = [PWM(Pin(pin)) for pin in led_pins]
for pwm in pwm_leds:
    pwm.freq(1000)

# potentiometer input GP26/ADC0
potentiometer = ADC(26)

while True:
    # read the potentiometer value (0-65535)
    pot_value = potentiometer.read_u16()

    # map the potentiometer value to the number of LEDs
    num_leds_on = int(pot_value / 6553.5)

    # map the potentiometer value to brightness
    brightness = int(pot_value)

    # turn on LEDs based on the number and control brightness with PWM
    for i in range(10):
        if i < num_leds_on:
            pwm_leds[i].duty_u16(brightness)
        else:
            pwm_leds[i].duty_u16(0)
            
    # convert the ADC value to a percentage
    percentage = int(pot_value / (65535 / 100))
    
    # print the percentage value
    print(f"Brightness Percentage: {percentage}%")

    utime.sleep(0.1)  # small delay for smooth updates
