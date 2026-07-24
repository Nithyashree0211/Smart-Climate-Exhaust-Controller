"""
sensor.py
Reads data from the DHT11 sensor and stores recent values.
"""

import time
import threading
from collections import deque
import RPi.GPIO as GPIO

from config import (
    DHT_PIN,
    DEFAULT_TEMP,
    DEFAULT_HUMIDITY,
    GRAPH_POINTS,
    SENSOR_INTERVAL
)

current_temp = DEFAULT_TEMP
current_hum = DEFAULT_HUMIDITY

temp_data = deque([DEFAULT_TEMP] * GRAPH_POINTS, maxlen=GRAPH_POINTS)
hum_data = deque([DEFAULT_HUMIDITY] * GRAPH_POINTS, maxlen=GRAPH_POINTS)


def read_dht11():
    """Continuously read the DHT11 sensor."""
    global current_temp, current_hum

    while True:
        data = []

        try:
            GPIO.setup(DHT_PIN, GPIO.OUT)
            GPIO.output(DHT_PIN, GPIO.LOW)
            time.sleep(0.02)

            GPIO.output(DHT_PIN, GPIO.HIGH)
            GPIO.setup(DHT_PIN, GPIO.IN)

            timeout = time.time() + 1

            while GPIO.input(DHT_PIN) == 1:
                if time.time() > timeout:
                    raise Exception

            while GPIO.input(DHT_PIN) == 0:
                if time.time() > timeout:
                    raise Exception

            while GPIO.input(DHT_PIN) == 1:
                if time.time() > timeout:
                    raise Exception

            for _ in range(40):
                t2 = time.time() + 1

                while GPIO.input(DHT_PIN) == 0:
                    if time.time() > t2:
                        raise Exception

                start = time.time()

                while GPIO.input(DHT_PIN) == 1:
                    if time.time() > t2:
                        raise Exception

                duration = time.time() - start
                data.append(1 if duration > 0.00005 else 0)

            bytes_data = []

            for i in range(5):
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | data[i * 8 + j]
                bytes_data.append(byte)

            checksum = (
                bytes_data[0]
                + bytes_data[1]
                + bytes_data[2]
                + bytes_data[3]
            ) & 0xFF

            if checksum == bytes_data[4]:
                current_temp = bytes_data[2]
                current_hum = bytes_data[0]

                temp_data.append(current_temp)
                hum_data.append(current_hum)

        except Exception:
            pass

        time.sleep(SENSOR_INTERVAL)


def start_sensor():
    """Start sensor reading thread."""
    thread = threading.Thread(target=read_dht11)
    thread.daemon = True
    thread.start()
