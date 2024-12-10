from gpiozero import Button, PWMLED
from signal import pause
import time

# Rotary Encoder Configurations
encoders = [
    {"clk": Button(16, pull_up=True), "dt": Button(20, pull_up=True), "sw": Button(21, pull_up=True), "led": PWMLED(26), "position": 0, "state": True},
    {"clk": Button(23, pull_up=True), "dt": Button(24, pull_up=True), "sw": Button(25, pull_up=True), "led": PWMLED(19), "position": 0, "state": True},
    {"clk": Button(17, pull_up=True), "dt": Button(27, pull_up=True), "sw": Button(22, pull_up=True), "led": PWMLED(13), "position": 0, "state": True},
    {"clk": Button(5, pull_up=True), "dt": Button(6, pull_up=True), "sw": Button(12, pull_up=True), "led": PWMLED(18), "position": 0, "state": True},
    {"clk": Button(14, pull_up=True), "dt": Button(15, pull_up=True), "sw": Button(4, pull_up=True), "led": PWMLED(22), "position": 0, "state": True},
]

# Adjust brightness for a specific encoder
def adjust_brightness(encoder):
    if encoder["state"]:  # Only adjust brightness if the LED is on
        brightness = encoder["position"] / 100
        encoder["led"].value = brightness
        print(f"LED on GPIO {encoder['led'].pin.number}: Position {encoder['position']}, Brightness {brightness:.2f}")

# Rotate handler for all encoders
def rotate(encoder):
    if encoder["clk"].is_pressed != encoder["dt"].is_pressed:
        if encoder["position"] < 100:
            encoder["position"] += 1
    else:
        if encoder["position"] > 0:
            encoder["position"] -= 1
    adjust_brightness(encoder)

# Button press handler for toggling LEDs
def toggle_led(encoder):
    encoder["state"] = not encoder["state"]
    if encoder["state"]:
        adjust_brightness(encoder)  # Restore brightness
        print(f"LED on GPIO {encoder['led'].pin.number}: ON")
    else:
        encoder["led"].off()
        print(f"LED on GPIO {encoder['led'].pin.number}: OFF")
    time.sleep(0.5)

# Assign callbacks to each encoder
for encoder in encoders:
    encoder["clk"].when_pressed = lambda e=encoder: rotate(e)
    encoder["sw"].when_pressed = lambda e=encoder: toggle_led(e)

# Run indefinitely
print("Rotary Encoder Program Running...")
pause()
