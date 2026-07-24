# Smart-Climate-Exhaust-Controller
Smart Climate &amp; Exhaust Controller for Hazardous Enclosures using Raspberry Pi 4
# Smart Climate & Exhaust Controller for Hazardous Enclosures

## Overview

The Smart Climate & Exhaust Controller is an IoT-based industrial safety system developed using Raspberry Pi 4. It continuously monitors temperature and humidity inside hazardous electrical enclosures, calculates the dew point, and automatically controls an exhaust fan using PWM to maintain safe operating conditions.

The system provides real-time monitoring through a 7-inch touchscreen HMI and supports manual override using hardware switches. LED indicators display the enclosure status, allowing operators to quickly identify normal, warning, and critical conditions.

---

## Features

- Real-time Temperature Monitoring
- Real-time Humidity Monitoring
- Dew Point Calculation
- Automatic PWM Fan Speed Control
- Manual Override Mode
- Three-Level LED Status Indication
- Live Graphs on Touchscreen
- Raspberry Pi Based Edge Processing
- Industrial Enclosure Protection

---

## Hardware Used

- Raspberry Pi 4 Model B
- DHT11 Temperature & Humidity Sensor
- 7-inch HDMI Touchscreen
- DC Exhaust Fan
- IRLZ44N MOSFET
- 1N4007 Flyback Diode
- Red, Yellow and Green LEDs
- Push Buttons
- Breadboard and Jumper Wires
- 1KΩ and 10KΩ Resistors

---

## Software Used

- Python 3
- Tkinter
- RPi.GPIO
- Flask (for future mobile dashboard)
- Threading

---

## Working Principle

1. Read temperature and humidity from the DHT11 sensor.
2. Calculate the dew point.
3. Classify enclosure condition as Normal, Warning, or Danger.
4. Control the exhaust fan speed using PWM.
5. Update LED indicators.
6. Display live data and graphs on the touchscreen.
7. Allow manual override using hardware buttons.

---

## Project Structure

```
project.py
README.md
requirements.txt
LICENSE
.gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Climate-Exhaust-Controller.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python project.py
```

---

## Applications

- Electrical Control Panels
- Industrial Enclosures
- Battery Storage Systems
- Server Cabinets
- Hazardous Equipment Rooms
- Factory Automation

---

## Future Improvements

- Cloud Data Logging
- Mobile App
- AI-Based Predictive Cooling
- SMS and Email Alerts
- MQTT Integration
- Industrial Grade Sensors

---

## Team

Hackathon Project

---

## License

This project is licensed under the MIT License.
