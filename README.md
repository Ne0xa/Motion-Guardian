# Intelligent Alarm System – Raspberry Pi Pico WH

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Pico%20W-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)
![MicroPython](https://img.shields.io/badge/MicroPython-2B2728?style=for-the-badge&logo=micropython&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-System-blue?style=for-the-badge&logo=homeassistant&logoColor=white)

## 📝 Description du Projet

This project implements an intelligent and connected alarm system built for the Raspberry Pi Pico W.
The system uses an ultrasonic sensor to detect intrusions, triggers both sound and light alarms, and can be deactivated using a PIN code entered on a numpad.
A web interface allows you to remotely monitor the alarm status over WiFi.

## ✨ Fonctionnalités

- **Automatic intrusion detection** using an HC-SR04 ultrasonic sensor
- **Multi-sensory alarm** : buzzer + RGB LED
- **Secure authentication** using 4‑digit PIN code on a numpad
- **Real-time web interface** for remote monitoring
- **Visual indicators** : green LED (idle), red LED (alarm active)
- **Software debouncing** to prevent repeated key presses
- **Timeout system** for ultrasonic sensor

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|-------------|---------|-------------|
| **MicroPython** | Latest | Firmware and programming language |
| **Raspberry Pi Pico W** | - | Microcontroller with integrated WiFi |
| **HTML** | 5 | Web monitoring interface |

### Hardware

- **HC-SR04** - Ultrasonic distance sensor (détection 2-400 cm)
- **Numppad** - PIN code entry
- **RGB LED** - Visual status indicator
- **Buzzer** - Sound alarm

### MicroPython APIs & Protocols

- **GPIO (General Purpose Input/Output)** - Hardware communication
- **PWM (Pulse Width Modulation)** - Buzzer/LED control
- **Socket API** - HTTP web server
- **WLAN** - WiFi 802.11 b/g/n (2.4 GHz)

### Libraries Used

```python
from machine import Pin, PWM   # GPIO and PWM control
import utime                   # Time management
import network                 # WiFi connection
import socket                  # HTTP web server
```

## 📌 Wiring Diagram

### HC-SR04 Ultrasonic Sensor
- **Trigger** → GPIO 2
- **Echo** → GPIO 3
- **VCC** → 5V
- **GND** → GND

### Buzzer
- **Signal** → GPIO 15
- **GND** → GND

### RGB LED
- **Red** → GPIO 16
- **Green** → GPIO 17
- **Blue** → GPIO 18
- **GND/VCC** → GND/3.3V (depending on type)

### Numpad

**Rows**
- Row 1 → GPIO 6
- Row 2 → GPIO 7
- Row 3 → GPIO 8
- Row 4 → GPIO 9

**Cols**
- Column 1 → GPIO 10
- Column 2 → GPIO 11
- Column 3 → GPIO 12
- Column 4 → GPIO 13

## 🚀 Installation & Launch

### Requirements

- Raspberry Pi Pico WH
- MicroPython installed on the Pico
- Compatible IDE (Thonny, VS Code with Pico extension, etc.)
- All required electronic components

### Installation Steps

```bash
# Clone the repository
git clone git@github.com:Ne0xa/IIM-B1-Motion-Guardian.git

# Navigate to the project folder
cd IIM-B1-Motion-Guardian
```

### Configuration

1. Open the main file in your IDE
2. Adjust configuration parameters:

```python
# Default PIN code
secret_code = "2704"

# Detection distance in cm
max_distance = 20

# WiFi
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"
```

### Launch

1. Connect all components according to the wiring diagram
2. Upload the code to your Raspberry Pi Pico WH
3. Open the serial monitor to retrieve the IP address
4. The system starts automatically

## 💡 Usage

### Normal Operation

1. **Idle mode** : green LED on, system ready
2. **Intrusion detection** : 
   - Object detected below 20 cm
   - LED turns red
   - Buzzer activates
3. **Deactivation** :
   - Enter the PIN code on the numpad
   - Press # to validate (or wait for auto-validation after 4 digits)
   - Press * to clear current input

### Web Interface

Once connected to WiFi, open the displayed IP address:
```
http://[PICO_IP_ADDRESS]
```

The interface shows the current alarm status (ON/OFF).

## 🎯 Technical Specifications

- **PWM frequency** : 1000 Hz (buzzer and LEDs)
- **PWM resolution** : 16 bits (0-65535)
- **Refresh rate** : 100 ms (10 Hz)
- **Sensor timeout** : 30 ms
- **Key debounce** : 300 ms
- **Web server port** : 80 (HTTP)
- **Sensor range** : 2-400 cm
- **Detection distance** : configurable (default 20 cm)

## 🔐 Security

- ✅ 4‑digit PIN code
- ✅ Masked input (*)
- ✅ Automatic reset after validation
- ✅ Key debouncing

⚠️ **Important** : Change the default PIN code (1234) before using the system in real situations

## 🛠️ Customization

### Change Detection Distance
```python
max_distance = 30  # Detect at 30 cm instead of 20 cm
```

### Change PIN Code
```python
secret_code = "1234"  
```

### Adjust Buzzer Frequency
```python
buzzer.freq(2000)  # Higher pitch
```

### Customize LED Colors
```python
def color(r, g, b):
    red.duty_u16(int(65535 * r))
    green.duty_u16(int(65535 * g))
    blue.duty_u16(int(65535 * b))
```

## 🐛  Troubleshooting

| Issue | Solution |
|----------|----------|
| **Sensor not detecting** | Check Trigger/Echo wiring and 5 V power |
| **WiFi not connecting** | Check SSID/password and ensure 2.4 GHz WiFi |
| **Numpad not responding** | Verify row/column connections |
| **Buzzer silent** | Check GPIO 15 wiring |
| **LED inactive** | Check LED type (common anode/cathode) and wiring |
| **Sensor timeout error** | Reduce timeout or check obstacles |

## 📊 Code Structure

```
├── GPIO Initialization
│   ├── Ultrasonic sensor (Trigger, Echo)
│   ├── Buzzer (PWM)
│   ├── RGB LED (PWM)
│   └── Numpad (4×4)
│
├── Main Functions
│   ├── maxDistance() – Ultrasonic distance measurement
│   ├── digitCode() – Keypad reading
│   ├── verifyCode() – PIN code validation
│   ├── readKey() – Key handling
│   └── color() – RGB LED control
│
├── Main Loop
│   ├── Distance measurement
│   ├── Intrusion detection
│   ├── Alarm handling
│   └── PIN code input
│
└── Web Server
    ├── WiFi connection
    └── HTML status page
```

## 📚 Resources

- [Documentation MicroPython](https://docs.micropython.org/)
- [Raspberry Pi Pico W Datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf)
- [HC-SR04 Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)

## 👨‍🎓 Academic Context

**Cours**: IOT  
**Niveau**: [First-year bachelor]  
**Établissement**: [IIM-Digital School]  
**Semestre**: [B1]

## 📄 Licence

This project was developed as part of an academic assignment. All rights reserved to the student.
