# config.py
# GPIO Pin Configuration for Smart Climate & Exhaust Controller

# DHT11 Sensor
DHT_PIN = 23

# LED Pins
RED_PIN = 27
YELLOW_PIN = 25
GREEN_PIN = 24

# Push Buttons
SW1_PIN = 5      # Manual Mode
SW2_PIN = 6      # Auto Mode

# PWM Fan
FAN_PIN = 18

# PWM Settings
PWM_FREQUENCY = 100

# Temperature Thresholds (°C)
NORMAL_TEMP = 30
WARNING_TEMP = 35

# Default Sensor Values
DEFAULT_TEMP = 28
DEFAULT_HUMIDITY = 45

# Graph Settings
GRAPH_POINTS = 50
GRAPH_WIDTH = 450
GRAPH_HEIGHT = 340

# GUI Settings
WINDOW_TITLE = "Smart Climate Controller"
BACKGROUND_COLOR = "black"
UPDATE_INTERVAL = 1000  # milliseconds
SENSOR_INTERVAL = 2      # seconds
