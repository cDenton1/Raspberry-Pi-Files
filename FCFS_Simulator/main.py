# FCFS (First Come First Serve) Simulator
from FCFS_Sim.LCD_display import lcd_init, lcd_line1, lcd_line2, lcd_clear, lcd_write_line
from FCFS_Sim.Rot_Enc import rotation, button
from FCFS_Sim.LED_bar import bar_clear, show_queue
import time
import sys

def grab_value():
    value = 0
    last_value = -1

    while True:
        delta = rotation()

        if delta != 0:
            value += delta

            if value < 0:
                value = 0
            if value > 10:
                value = 10

        if value != last_value:
            lcd_write_line(lcd_line2, "       {:02d}       ".format(value))
            last_value = value

        if button():
            break

        time.sleep(0.01)

    return value

def run_process(burst):
    for i in range(burst):
        set_led(i)
        time.sleep(1)
    bar_clear()

lcd_init()

current_time = 0
queue = []
running = None
exec_prog = 0

bar_clear()

lcd_clear()
time.sleep(0.002)

lcd_write_line(lcd_line1, " FCFS Simulator")
time.sleep(0.05)
lcd_write_line(lcd_line2, "  Click to Run")

while not button():
    time.sleep(0.01)

lcd_clear()
time.sleep(0.02)
lcd_write_line(lcd_line1, "Process Amount:") # ask user for process amount

lcd_write_line(lcd_line2, "       00 ")
numProcesses = grab_value()

if numProcesses < 2:
    lcd_clear()
    time.sleep(0.02)
    
    lcd_write_line(lcd_line1, "Not enough")
    lcd_write_line(lcd_line2, "processes, bye!")
    
    time.sleep(1)
    lcd_clear()
    sys.exit()

processes = []
for proc in range(numProcesses):
    lcd_clear()
    time.sleep(0.02)
    lcd_write_line(lcd_line1, f"PID {proc + 1:02d} Arrival:") # ask user for process amount
    
    lcd_write_line(lcd_line2, "       00 ")
    aTime = grab_value()
    
    lcd_clear()
    time.sleep(0.02)
    lcd_write_line(lcd_line1, f" PID {proc + 1:02d} Burst:") # ask user for process amount

    lcd_write_line(lcd_line2, "       00 ")
    bTime = grab_value()
    
    processes.append({
        "pid": proc + 1,
        "arrival": aTime,
        "burst": bTime,
        "comp": 0
    })
    
processes.sort(key=lambda p: (p["arrival"],  p["pid"]))
    
lcd_clear()
time.sleep(0.02)

while True:
    for p in processes:
        if p["arrival"] == current_time:
            queue.insert(0, p["pid"])
            lcd_write_line(lcd_line2, f"PID {p['pid']} arrived")
            show_queue(queue)

    if running is None and queue:
            running = queue[-1]
            exec_prog = 0

    if running is not None:
        proc = None
        for p in processes:
            if p["pid"] == running:
                proc = p
                break
        exec_prog += 1
        
        lcd_write_line(lcd_line1, f"T:{current_time:02d}")
        
        # lcd_write_line(lcd_line2, f"PID {proc['pid']} run {exec_prog}")
        
        if exec_prog >= proc["burst"]:
            lcd_write_line(lcd_line2, f"PID {proc['pid']} done")
            proc["comp"] = current_time + 1
            
            queue.pop()
            running = None
            exec_prog = 0
    else:
        lcd_write_line(lcd_line2, "Idle")
    
    done = True
    for p in processes:
        if p["arrival"] > current_time or queue or running:
            done = False
    
    if done:
        break

    show_queue(queue)
    current_time += 1
    time.sleep(1)
    
total_waiting = 0
total_turnaround = 0

for p in processes:
    turnaround = p['comp'] - p['arrival']
    waiting = turnaround - p['burst']
    
    total_waiting += waiting
    total_turnaround += turnaround

avg_waiting = total_waiting / len(processes)
avg_turnaround = total_turnaround / len(processes)

lcd_clear()
time.sleep(0.02)

lcd_write_line(lcd_line1, f"Waiting: {avg_waiting}")
lcd_write_line(lcd_line2, f"Turnaround: {avg_turnaround}")

time.sleep(5)

lcd_clear()
bar_clear()

