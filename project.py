import RPi.GPIO as GPIO
import time
import threading
import tkinter as tk
from collections import deque

DHT_PIN = 23
RED_PIN = 27
YELLOW_PIN = 25
GREEN_PIN = 24
SW1_PIN = 5
SW2_PIN = 6
FAN_PIN = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(SW1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(RED_PIN, GPIO.LOW)
GPIO.output(YELLOW_PIN, GPIO.LOW)
GPIO.output(GREEN_PIN, GPIO.LOW)

fan = GPIO.PWM(FAN_PIN, 100)
fan.start(0)

mode = "AUTO"
current_temp = 28
current_hum = 45
temp_data = deque([28]*50, maxlen=50)
hum_data = deque([45]*50, maxlen=50)

def read_dht11():
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
                    raise Exception("t")
            while GPIO.input(DHT_PIN) == 0:
                if time.time() > timeout:
                    raise Exception("t")
            while GPIO.input(DHT_PIN) == 1:
                if time.time() > timeout:
                    raise Exception("t")
            for i in range(40):
                t2 = time.time() + 1
                while GPIO.input(DHT_PIN) == 0:
                    if time.time() > t2:
                        raise Exception("t")
                start = time.time()
                while GPIO.input(DHT_PIN) == 1:
                    if time.time() > t2:
                        raise Exception("t")
                duration = time.time() - start
                data.append(1 if duration > 0.00005 else 0)
            bytes_data = []
            for i in range(5):
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | data[i*8+j]
                bytes_data.append(byte)
            if ((bytes_data[0]+bytes_data[1]+bytes_data[2]+bytes_data[3])&0xFF)==bytes_data[4]:
                current_temp = bytes_data[2]
                current_hum = bytes_data[0]
                temp_data.append(current_temp)
                hum_data.append(current_hum)
        except:
            pass
        time.sleep(2)

def all_leds_off():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)

def update():
    global mode
    if GPIO.input(SW1_PIN) == GPIO.LOW:
        time.sleep(0.05)
        if GPIO.input(SW1_PIN) == GPIO.LOW:
            mode = "MANUAL"
    elif GPIO.input(SW2_PIN) == GPIO.LOW:
        time.sleep(0.05)
        if GPIO.input(SW2_PIN) == GPIO.LOW:
            mode = "AUTO"
    all_leds_off()
    if mode == "MANUAL":
        GPIO.output(RED_PIN, GPIO.HIGH)
        fan.ChangeDutyCycle(100)
        status = "MANUAL OVERRIDE"
        color = "red"
        fan_speed = "100%"
    elif current_temp < 30:
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        fan.ChangeDutyCycle(30)
        status = "NORMAL"
        color = "green"
        fan_speed = "50%"
    elif current_temp < 35:
        GPIO.output(YELLOW_PIN, GPIO.HIGH)
        fan.ChangeDutyCycle(60)
        status = "WARNING"
        color = "yellow"
        fan_speed = "70%"
    else:
        GPIO.output(RED_PIN, GPIO.HIGH)
        fan.ChangeDutyCycle(100)
        status = "DANGER"
        color = "red"
        fan_speed = "100%"
    dew = round(current_temp - ((100-current_hum)/5), 1)
    temp_label.config(text=f"Temperature: {current_temp} C")
    hum_label.config(text=f"Humidity: {current_hum} %")
    dew_label.config(text=f"Dew Point: {dew} C")
    status_label.config(text=f"Status: {status}", fg=color)
    mode_label.config(text=f"Mode: {mode}")
    fan_label.config(text=f"Fan Speed: {fan_speed}")
    canvas.delete("all")
    tlist = list(temp_data)
    canvas.create_text(225, 15, text="Temperature (C)", fill="red", font=("Arial", 11, "bold"))
    for i in range(len(tlist)-1):
        x1 = i*8
        x2 = (i+1)*8
        y1 = 30+120-(tlist[i]/60)*120
        y2 = 30+120-(tlist[i+1]/60)*120
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
    canvas.create_line(0, 30+120-(30/60)*120, 400, 30+120-(30/60)*120, fill="orange", dash=(4,4))
    canvas.create_text(415, 30+120-(30/60)*120, text="30C", fill="orange", font=("Arial", 8))
    canvas.create_line(0, 30+120-(35/60)*120, 400, 30+120-(35/60)*120, fill="red", dash=(4,4))
    canvas.create_text(415, 30+120-(35/60)*120, text="35C", fill="red", font=("Arial", 8))
    hlist = list(hum_data)
    canvas.create_text(225, 175, text="Humidity (%)", fill="blue", font=("Arial", 11, "bold"))
    for i in range(len(hlist)-1):
        x1 = i*8
        x2 = (i+1)*8
        y1 = 190+120-(hlist[i]/100)*120
        y2 = 190+120-(hlist[i+1]/100)*120
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
    root.after(1000, update)

t = threading.Thread(target=read_dht11)
t.daemon = True
t.start()

root = tk.Tk()
root.title("Smart Climate Controller")
root.attributes('-fullscreen', True)
root.configure(bg="black")
temp_label = tk.Label(root, text="Temperature: -- C", font=("Arial", 20, "bold"), fg="red", bg="black")
temp_label.pack(pady=3)
hum_label = tk.Label(root, text="Humidity: -- %", font=("Arial", 20, "bold"), fg="blue", bg="black")
hum_label.pack(pady=3)
dew_label = tk.Label(root, text="Dew Point: -- C", font=("Arial", 16), fg="cyan", bg="black")
dew_label.pack(pady=3)
status_label = tk.Label(root, text="Status: --", font=("Arial", 18, "bold"), fg="green", bg="black")
status_label.pack(pady=3)
mode_label = tk.Label(root, text="Mode: AUTO", font=("Arial", 14), fg="white", bg="black")
mode_label.pack(pady=3)
fan_label = tk.Label(root, text="Fan Speed: -- %", font=("Arial", 14), fg="white", bg="black")
fan_label.pack(pady=3)
canvas = tk.Canvas(root, width=450, height=340, bg="black", highlightthickness=0)
canvas.pack(pady=3)
quit_btn = tk.Button(root, text="QUIT", font=("Arial", 14, "bold"), fg="white", bg="red", command=root.destroy)
quit_btn.pack(pady=5)
root.after(1000, update)

try:
    root.mainloop()
finally:
    all_leds_off()
    fan.stop()
    GPIO.cleanup()
    print("Stopped!")
