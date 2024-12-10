from gpiozero import Button, PWMLED
from signal import pause
import time
import speech_recognition as sr

# Initialize speech recognizer
recognizer = sr.Recognizer()

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

# Voice control function
def voice_control():
    with sr.Microphone() as source:
        print("Listening for a command...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")

            # Parse commands for LEDs
            for i, encoder in enumerate(encoders, start=1):
                if f"led {i}" in command:
                    if "on" in command:
                        encoder["state"] = True
                        adjust_brightness(encoder)
                        print(f"LED {i}: ON via voice")
                    elif "off" in command:
                        encoder["state"] = False
                        encoder["led"].off()
                        print(f"LED {i}: OFF via voice")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Main loop
try:
    print("Rotary Encoder Program Running...")
    while True:
        voice_control()
except KeyboardInterrupt:
    print("Program terminated.")
