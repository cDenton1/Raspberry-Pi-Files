# Raspberry Pi Files
Included in this repository are files that I've programmed or used for my Raspberry Pi Pico W, either for class or personal projects. <br>

## Projects
### 1. Coin Flip Game
OLED-CoinFlipGame.py - Requires an OLED Display, and x2 Buttons
- User calls heads or tails via the buttons
- The OLED displays any required ouput, which includes
  - The users call
  - The flip animation of the coin
  - The side it lands on
  - Whether the user was right or not
- The landed side is randomized, and the code doesn't loop
- Demonstration - <a href="https://youtu.be/iaiqS3QNyAw?si=wklGf-frqKPXHuVz">Coin Flip | Raspberry Pi Pico W</a>

### 2. Potentiometer Graph
10SegDisplay-PMGraph.py - Requires a 10 Segment Bar Graph Display, Rotary Potentiometer, and PWM (Pulse Width Module)
- The brightness of the bar graph is adjusted by rotating the potentiometer (PM)
  - Rotating clockwise will brighten the LEDs from one side to the other
  - Rotating counter-clockwise will dim the LEDs the other way
- The value of the PM is mapped to each LED and the brightness of the display
- The PM value is displayed to the terminal as a percentage
- Demonstration - <a href="https://youtu.be/pedJWBaIUEM?si=cL0R3xNyznI9KKEP">Potentiometer and Bar Graph Display | Raspberry Pi Pico W</a>

### 3. Memory Game
MemoryGame.py - Requires x3 Buttons, and x3 LEDs (preferably all different colours)
- A sequence of LEDs are flashed, a new random LED is added each round
- User presses the corresponding buttons of the LEDs to repeat the sequence flashed at them
- Cycle repeats until the user gets one wrong
  - If correct, "Correct!" is printed to the terminal before continuing
  - If wrong, "Wrong! Game Over!" is printed to the terminal, all LEDs loop through flashing, and the program exits

### 4. Water Level Monitor
FinalProj305.py - Requires a Water Sensor, OLED Display, buzzer, and x2 LEDs (preferably red and green)
- Tracks the water level with a preset low and high threshold using a water sensor
- Connected to the internet, it sends the data to ThingSpeak to graph it
- Outputs the water level detected and the corresponding status to the OLED display <br>

| Level                  |  Status  | Output             |
|------------------------|----------|--------------------|
| Below Lower Threshold  | LOW      | Red LED and Buzzer |
| Between Thresholds     | OK       | Green LED          |
| Above Higher Threshold | HIGH     | Red LED and Buzzer |

- Demonstration - <a href="https://youtu.be/hNhDl3mNzno">Water Level Monitor | ITSC-305 Final Project</a>

## Usage
To run any code on a Raspberry Pi Pico you're going to need **MicroPython** and an **IDE** that can work with your Pi. Most notable is, <a href="https://thonny.org/">Thonny</a>, as it's free and well documented, finding any tutorials regarding setup is extremely easy. <br> 
For any programs requiring the **OLED Display**, the file **ssd1306.py** is necessary for it to work properly. It's provided here in this repository for ease of access, but it can also be found online, along with documentation for setup, and tutorials, or on my blog.

## More Information
To go more in-depth on a couple of these programs, I would recommend checking out my blog, <a href="https://my-cybersec-journey.hashnode.dev/">My Cybersecurity Journey</a>. In my article, <a href="https://my-cybersec-journey.hashnode.dev/raspberry-pi-pico">My Experience With a Raspberry Pi Pico</a>, I dive into a couple of the programs, walking through the setup and explaining the code. I also share why I'm using a Pi, my initial thoughts, and overall first experience. <br>
