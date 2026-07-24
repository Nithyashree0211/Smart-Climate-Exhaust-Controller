"""
controller.py
Controls LEDs, PWM fan and operating mode.
"""

import RPi.GPIO as GPIO

from config import (
    RED_PIN,
    YELLOW_PIN,
    GREEN_PIN,
    SW1_PIN,
    SW2_PIN,
    FAN_PIN,
    PWM_FREQUENCY,
)

from sensor import current_temp
from utils import get_status

# Current operating mode
mode = "AUTO"

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

GPIO.setup(SW1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(FAN_PIN, GPIO.OUT)

fan = GPIO.PWM(FAN_PIN, PWM_FREQUENCY)
fan.start(0)


def all_leds_off():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)


def update_controller():
    """
    Reads buttons, updates mode,
    controls LEDs and fan.

    Returns:
        mode, status, fan_speed
    """

    global mode

    # Manual Mode
    if GPIO.input(SW1_PIN) == GPIO.LOW:
        mode = "MANUAL"

    # Auto Mode
    elif GPIO.input(SW2_PIN) == GPIO.LOW:
        mode = "AUTO"

    all_leds_off()

    if mode == "MANUAL":
        GPIO.output(RED_PIN, GPIO.HIGH)
        fan.ChangeDutyCycle(100)
        return mode, "MANUAL OVERRIDE", 100

    status, speed, led = get_status(current_temp)

    fan.ChangeDutyCycle(speed)

    if led == "GREEN":
        GPIO.output(GREEN_PIN, GPIO.HIGH)

    elif led == "YELLOW":
        GPIO.output(YELLOW_PIN, GPIO.HIGH)

    else:
        GPIO.output(RED_PIN, GPIO.HIGH)

    return mode, status, speed


def cleanup():
    """Safely stop hardware."""
    all_leds_off()
    fan.stop()
    GPIO.cleanup()
