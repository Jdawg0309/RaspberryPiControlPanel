from gpiozero import Button, PWMLED
from signal import pause
import time

# Encoder 1 pins
clk1 = Button(16, pull_up=True)  # GPIO16
dt1 = Button(20, pull_up=True)   # GPIO20
sw1 = Button(21, pull_up=True)   # GPIO21
light1 = PWMLED(26)              # GPIO26 for Light 1

# Encoder 2 pins
clk2 = Button(23, pull_up=True)  # GPIO23
dt2 = Button(24, pull_up=True)   # GPIO24
sw2 = Button(25, pull_up=True)   # GPIO25
light2 = PWMLED(19)              # GPIO19 for Light 2

# Encoder 3 pins
clk3 = Button(17, pull_up=True)  # GPIO17
dt3 = Button(27, pull_up=True)   # GPIO27
sw3 = Button(22, pull_up=True)   # GPIO22
light3 = PWMLED(13)              # GPIO13 for Light 3

# Position tracking with max value 0-100
position1 = 0
position2 = 0
position3 = 0

# Functions to handle rotation and update brightness
def rotate1():
    global position1
    if clk1.is_pressed != dt1.is_pressed:
        if position1 < 100:
            position1 += 1
    else:
        if position1 > 0:
            position1 -= 1
    brightness = position1 / 100  # Scale position to a value between 0 and 1
    light1.value = brightness
    print(f"Encoder 1 Position: {position1}, Brightness: {brightness:.2f}")

def rotate2():
    global position2
    if clk2.is_pressed != dt2.is_pressed:
        if position2 < 100:
            position2 += 1
    else:
        if position2 > 0:
            position2 -= 1
    brightness = position2 / 100  # Scale position to a value between 0 and 1
    light2.value = brightness
    print(f"Encoder 2 Position: {position2}, Brightness: {brightness:.2f}")

def rotate3():
    global position3
    if clk3.is_pressed != dt3.is_pressed:
        if position3 < 100:
            position3 += 1
    else:
        if position3 > 0:
            position3 -= 1
    brightness = position3 / 100  # Scale position to a value between 0 and 1
    light3.value = brightness
    print(f"Encoder 3 Position: {position3}, Brightness: {brightness:.2f}")

# Assign callbacks for rotation
clk1.when_pressed = rotate1
clk2.when_pressed = rotate2
clk3.when_pressed = rotate3

# Run indefinitely
print("Rotary Encoder Program Running...")
pause()
