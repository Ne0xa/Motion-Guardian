from machine import Pin, PWM
import utime
import network
import socket

# --- WiFi Configuration---
SSID = "YOUR_WIFI_NAME" # WiFi name
PASSWORD = "YOUR_WIFI_PASSWORD" # WiFi password

# --- Ultrasonic sensor ---
trigger = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)

# --- Buzzer ---
buzzer = PWM(Pin(15))
buzzer.freq(1000)
buzzer.duty_u16(0)

# --- LED RGB ---
red = PWM(Pin(16))
green = PWM(Pin(17))
blue = PWM(Pin(18))

for led in (red, green, blue):
    led.freq(1000)
    led.duty_u16(0)

def off():
    red.duty_u16(0)
    green.duty_u16(0)
    blue.duty_u16(0)

def color(r, g, b):
    red.duty_u16(65535 if r else 0)
    green.duty_u16(65535 if g else 0)
    blue.duty_u16(65535 if b else 0)

# --- Matrix keypad ---
rows = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
cols = [Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN),
        Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(13, Pin.IN, Pin.PULL_DOWN)]

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# --- Settings ---
secret_code = "1234"
input = ""
max_distance = 20
active_alarm = False
notification = False

# --- WiFi connection ---
def wifi_connect():
    """Connect the Pico to WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi")
    timeout = 10
    while timeout > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        timeout -= 1
        print(".", end="")
        utime.sleep(1)

    if wlan.status() != 3:
        print("\nWiFi connection failed")
        return None
    else:
        print("\nConnected to WiFi")
        status = wlan.ifconfig()
        print(f"IP address: {status[0]}")
        return wlan

def web_page(distance, max_distance, active_alarm, input):
    etat = "Active alarm!" if active_alarm else "System OK"
    status_color = "#ff4444" if active_alarm else "#44ff44"

    html = f"""<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="2">
    <title>Alarm - Monitoring</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }}
        .card {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .status {{
            background: {status_color};
            color: white;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        }}
        .info {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .info p {{
            margin: 10px 0;
            font-size: 16px;
        }}
        .label {{
            font-weight: bold;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Alarm System</h1>
        <div class="status">{etat}</div>
        <div class="info">
            <p><span class="label">Distance detected:</span> {distance:.1f} cm</p>
            <p><span class="label">Alert threshold:</span> {max_distance} cm</p>
            <p><span class="label">Input code:</span> {'*' * input}</p>
            <p><span class="label">Expected code:</span> {len(secret_code)} digits</p>
        </div>
        <p style="text-align: center; color: #999; margin-top: 20px;"></p>
    </div>
</body>
</html>"""
    return html

# --- Functions ---
def maxDistance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()

    timeout = 30000

    start = utime.ticks_us()
    while echo.value() == 0:
        if utime.ticks_diff(utime.ticks_us(), start) > timeout:
            return -1
        start_time = utime.ticks_us()

    start = utime.ticks_us()
    while echo.value() == 1:
        if utime.ticks_diff(utime.ticks_us(), start) > timeout:
            return -1
        end_time = utime.ticks_us()

    timing = utime.ticks_diff(end_time, start_time)
    distance = (timing * 0.0343) / 2
    return distance

def activate_buzzer():
    buzzer.duty_u16(32768)
    print("active_buzzer")

def deactivate_buzzer():
    buzzer.duty_u16(0)
    #print("deactivate_buzzer")

def digitCode():
    for i, row in enumerate(rows):
        row.high()
        for j, col in enumerate(cols):
            if col.value():
                row.low()
                utime.sleep_ms(40)
                return keys[i][j]
        row.low()
    return None

def verifyCode():
    global input, active_alarm, notification
    if input == secret_code:
        print("Correct code! Alarm deactivated")
        deactivate_buzzer()
        active_alarm = False
        notification = False
        input = ""
        return True
    else:
        print("Incorrect code!")
        input = ""
        return False

def readKey(key):
    global input

    if key == '#':
        return verifyCode()

    elif key == '*':
        input = ""
        print("Code deleted")

    else:
        input += key
        print("Code: " + "*" * len(input))

        if len(input) == 4:
            return verifyCode()

    return False

# --- Main program ---
print("="*40)
print("Alarm system started")
print("="*40)

# WiFi connection
wlan = wifi_connect()
if wlan is None:
    print("ERROR: Cannot proceed without a WiFi connection")
    color(1, 0, 0)
    while True:
        utime.sleep(1)

# Starting server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.settimeout(0.2)

print(f"Web server started on: http://{wlan.ifconfig()[0]}")
print("Max distance:", max_distance, "cm")
print("PIN code:", secret_code)
print("="*40)

for i in range(10, 0, -1):
    print(f"Starting in {i} seconds...")
    utime.sleep(2)

print("\nAlarm system active!")
print("="*40)

latest_key = None
last_key_time = 0
current_distance = 0

last_client_display = 0
display_delay = 2000     


while True:
    distance = maxDistance()

    if distance != -1:
        current_distance = distance
        #print("Distance:", round(distance, 1), "cm")

        # --- Intrusion detection ---
        if distance < max_distance and not active_alarm:
            print("ALERT! Person detected!")
            color(1, 0, 0)       # Red LED
            activate_buzzer()     # Buzzer ON
            active_alarm = True
            notification = True

        # --- If alarm is active: digit code ---
        if active_alarm:
            key = digitCode()
            current_time = utime.ticks_ms()

            if key and (key != latest_key or utime.ticks_diff(current_time, last_key_time) > 300):
                print("Key pressed:", key)
                readKey(key)
                latest_key = key
                last_key_time = current_time

        # --- If no intrusion AND alarm is inactive ---
        if not active_alarm and distance >= max_distance:
            color(0, 1, 0)       # Green LED
            deactivate_buzzer()
            notification = False

    try:
        client, addr_client = s.accept()
        time = utime.ticks_ms()
        if utime.ticks_diff(time, last_client_display) > display_delay:
            print(f"Client connected from {addr_client}")
            last_client_display = time
        request = client.recv(1024)
        
        response = web_page(current_distance, max_distance, active_alarm, len(input))
        http_response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n\r\n' + response
        client.send(http_response)
        client.close()

    except OSError:
        pass

    utime.sleep_ms(2)

