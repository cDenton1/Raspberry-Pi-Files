# FCFS (First Come First Serve) Simulator
from FCFS_Sim.LCD_display import lcd_init, lcd_line1, lcd_line2, lcd_clear, lcd_write_line
from FCFS_Sim.Rot_Enc import rotation, button
from FCFS_Sim.LED_bar import bar_clear, show_queue
import time
import sys

def grab_value():  # function used for getting input from the rotary encoder
    value = 0
    last_value = -1

    while True:
        delta = rotation()  # call the rotation function in the rot_enc script 

        if delta != 0:
            value += delta  # change value based on the rotation

            if value < 0:   # value must stay 0 or above
                value = 0
            if value > 10:  # value must stay 10 or below
                value = 10

        if value != last_value:  # change the value output to the LCD display
            lcd_write_line(lcd_line2, "       {:02d}       ".format(value))
            last_value = value

        if button():  # when the button is pressed
            break     # break the while loop

        time.sleep(0.01)

    return value  # return the value

def run_process(burst):
    for i in range(burst):
        set_led(i)
        time.sleep(1)
    bar_clear()

lcd_init()  # initialize the LCD before running

current_time = 0  # set the current time to 0 - this tracks the time once running
queue = []        # create and empty list for the queue
running = None    # set the current running process to none
exec_prog = 0     # time for the execution progression

bar_clear()  # clear the bar graph display of any lights

lcd_clear()  # clear the LCD display of any output
time.sleep(0.002)

lcd_write_line(lcd_line1, " FCFS Simulator")  # print to line one the title text
time.sleep(0.05)
lcd_write_line(lcd_line2, "  Click to Run")   # print to line two how to progress 

while not button():  # wait for the button
    time.sleep(0.01)

lcd_clear()  # clear the LCD display
time.sleep(0.02)
lcd_write_line(lcd_line1, "Process Amount:") # ask user for process amount

lcd_write_line(lcd_line2, "       00 ") # print the initial zero of the counter
numProcesses = grab_value()  # call grab_value to store the amount of processes

if numProcesses < 2:  # if not enough processes
    lcd_clear()  # clear the LCD display
    time.sleep(0.02)

    # print a goodbye message and why before exiting
    lcd_write_line(lcd_line1, "Not enough")
    lcd_write_line(lcd_line2, "processes, bye!")
    
    time.sleep(1)
    lcd_clear()
    sys.exit()

processes = []  # create a list of dictonaries for the processes
for proc in range(numProcesses):  # loop through based on the amount decided by the user
    lcd_clear()  # clear the LCD display
    time.sleep(0.02)
    lcd_write_line(lcd_line1, f"PID {proc + 1:02d} Arrival:") # ask user for arrival time
    
    lcd_write_line(lcd_line2, "       00 ") # print the initial zero of the counter
    aTime = grab_value()  # call grab_value and store input
    
    lcd_clear()  # clear the LCD display
    time.sleep(0.02)
    lcd_write_line(lcd_line1, f" PID {proc + 1:02d} Burst:") # ask user for burst time

    lcd_write_line(lcd_line2, "       00 ") # print the initial zero of the counter
    bTime = grab_value()  # call grab_value and store input

    # append new process along with necessary values
    processes.append({
        "pid": proc + 1,
        "arrival": aTime,
        "burst": bTime,
        "comp": 0
    })

# sort processes based on arrival times and then process ID
processes.sort(key=lambda p: (p["arrival"],  p["pid"]))
    
lcd_clear()  # clear the LCD display
time.sleep(0.02)

while True:
    for p in processes:  # loop through processes
        if p["arrival"] == current_time:  # check if any arrived
            queue.insert(0, p["pid"])  # insert them into the queue
            lcd_write_line(lcd_line2, f"PID {p['pid']} arrived")  # print that a process arrives
            show_queue(queue)  # update visual queue

    if running is None and queue: # if no process is running and there is a queue
        running = queue[-1]  # update what is running
        exec_prog = 0  # reset the execution progress

    if running is not None:  # if a process is running
        proc = None  # set proc to none
        for p in processes:  # loop through processes
            if p["pid"] == running:  # find what is running
                proc = p  # set proc to the running process
                break  #break for loop
        exec_prog += 1  # update the execution progress
        
        lcd_write_line(lcd_line1, f"T:{current_time:02d}")  # update the current time output
        
        if exec_prog >= proc["burst"]:  # compare the execution progression with the process burst time
            lcd_write_line(lcd_line2, f"PID {proc['pid']} done")  # print the process is done
            proc["comp"] = current_time + 1  # update the completion time of the process
            
            queue.pop()  # pop the process from the queue
            running = None  # set running to none
            exec_prog = 0  # reset the execution progression
    else:
        lcd_write_line(lcd_line2, "Idle")  # print idle if nothing is running and nothing in the queue
    
    done = True  # set done to true
    for p in processes:  # loop through the processes
        if p["arrival"] > current_time or queue or running:
            done = False  # if anything has a time greater than the current time, set done to false
    
    if done:  # if done stays true
        break  # break the while loop

    show_queue(queue)  # update the visual queue
    current_time += 1  # update the current time
    time.sleep(1)  # wait one second
    
total_waiting = 0  # set total waiitng time to zero
total_turnaround = 0  # set total turnaround time to zero

for p in processes:  # loop through processes
    turnaround = p['comp'] - p['arrival']  # calculate turnaround
    waiting = turnaround - p['burst']  # calculate waiting
    
    total_waiting += waiting  # add to the total
    total_turnaround += turnaround  # add to the total

avg_waiting = total_waiting / len(processes)  # calculate the average
avg_turnaround = total_turnaround / len(processes)  # calculate the average

lcd_clear()  # clear the LCD display
time.sleep(0.02)

# output the averages of waiting and turnaround
lcd_write_line(lcd_line1, f"Waiting: {avg_waiting}")
lcd_write_line(lcd_line2, f"Turnaround: {avg_turnaround}")

time.sleep(5)

# clear both the bar graph and lcd display
lcd_clear()
bar_clear()
