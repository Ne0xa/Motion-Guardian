from machine import Pin, PWM
import utime

# --- Capteur ultrason ---
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

# --- Clavier matriciel ---
rows = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
cols = [Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN),
        Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(13, Pin.IN, Pin.PULL_DOWN)]

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# --- Paramètres ---
CODE_CORRECT = "2704"
code_saisi = ""
distance_max = 20
alarme_active = False

# --- Fonctions ---
def distanceMax():
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

    duree = utime.ticks_diff(end_time, start_time)
    distance = (duree * 0.0343) / 2
    return distance

def activer_buzzer():
    buzzer.duty_u16(32768)
    print("active_buzzer")

def desactiver_buzzer():
    buzzer.duty_u16(0)
    print("desactiver_buzzer")

def digiCode():
    for i, row in enumerate(rows):
        row.high()
        for j, col in enumerate(cols):
            if col.value() == 1:
                row.low()
                return keys[i][j]
        row.low()
    return None

def verifCode():
    global code_saisi, alarme_active
    if code_saisi == CODE_CORRECT:
        print("Code correct ! Alarme désactivée")
        desactiver_buzzer()
        alarme_active = False
        code_saisi = ""
        return True
    else:
        print("Code incorrect !")
        code_saisi = ""
        return False

def gereTouche(touche):
    global code_saisi

    if touche == '#':
        return verifCode()

    elif touche == '*':
        code_saisi = ""
        print("Code effacé")

    else:
        code_saisi += touche
        print("Code: " + "*" * len(code_saisi))

        if len(code_saisi) == 4:
            return verifCode()

    return False

# --- Programme principal ---
print("Système d'alarme démarré")
print("Distance max:", distance_max, "cm")
print("Code PIN:", CODE_CORRECT)

derniere_touche = None
temps_derniere_touche = 0

while True:
    distance = distanceMax()

    if distance != -1:
        print("Distance:", round(distance, 1), "cm")

        # --- Détection d'intrusion ---
        if distance < distance_max and not alarme_active:
            print("ALERTE ! Objet détecté !")
            color(1, 0, 0)       # LED rouge
            activer_buzzer()     # Buzzer ON
            alarme_active = True

        # --- Si alarme active : digicode ---
        if alarme_active:
            touche = digiCode()
            temps_actuel = utime.ticks_ms()

            if touche and (touche != derniere_touche or utime.ticks_diff(temps_actuel, temps_derniere_touche) > 300):
                print("Touche pressée:", touche)
                gereTouche(touche)
                derniere_touche = touche
                temps_derniere_touche = temps_actuel

        # --- Si pas d'intrusion et alarme inactive ---
        if not alarme_active and distance >= distance_max:
            color(0, 1, 0)       # LED verte
            desactiver_buzzer()

    utime.sleep_ms(100)
