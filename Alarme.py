from machine import Pin, PWM
import utime
import network
import socket

# --- Configuration WiFi ---
SSID = "YOUR_WIFI_NAME" # Nom du WiFi
PASSWORD = "YOUR_WIFI_PASSWORD" # mdp du WiFi

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
notification = False

# --- Connexion WiFi ---
def connecter_wifi():
    """Connecte le Pico au WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connexion au WiFi...")
    timeout = 10
    while timeout > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        timeout -= 1
        print(".", end="")
        utime.sleep(1)

    if wlan.status() != 3:
        print("\nEchec de connexion WiFi")
        return None
    else:
        print("\nConnecté au WiFi !")
        status = wlan.ifconfig()
        print(f"Adresse IP: {status[0]}")
        return wlan

def webpage(distance, distance_max, alarme_active, code_saisi):
    etat = "Alarme Active !" if alarme_active else "Système OK"
    couleur = "#ff4444" if alarme_active else "#44ff44"

    html = f"""<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="2">
    <title>Alarme - Surveillance</title>
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
            background: {couleur};
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
        <h1>Système d'Alarme</h1>
        <div class="status">{etat}</div>
        <div class="info">
            <p><span class="label">Distance détectée:</span> {distance:.1f} cm</p>
            <p><span class="label">Seuil d'alerte:</span> {distance_max} cm</p>
            <p><span class="label">Code saisi:</span> {'*' * code_saisi}</p>
            <p><span class="label">Code attendu:</span> {len(CODE_CORRECT)} chiffres</p>
        </div>
        <p style="text-align: center; color: #999; margin-top: 20px;"></p>
    </div>
</body>
</html>"""
    return html

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
    #print("desactiver_buzzer")

def digiCode():
    for i, row in enumerate(rows):
        row.high()
        for j, col in enumerate(cols):
            if col.value():
                row.low()
                utime.sleep_ms(40)
                return keys[i][j]
        row.low()
    return None

def verifCode():
    global code_saisi, alarme_active, notification
    if code_saisi == CODE_CORRECT:
        print("Code correct ! Alarme désactivée")
        desactiver_buzzer()
        alarme_active = False
        notification = False
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
print("="*40)
print("Système d'alarme démarré")
print("="*40)

# Connexion WiFi
wlan = connecter_wifi()
if wlan is None:
    print("ERREUR: Impossible de continuer sans WiFi")
    color(1, 0, 0)
    while True:
        utime.sleep(1)

# Démarrage du server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.settimeout(0.2)

print(f"Serveur web démarré sur http://{wlan.ifconfig()[0]}")
print("Distance max:", distance_max, "cm")
print("Code PIN:", CODE_CORRECT)
print("="*40)

for i in range(10, 0, -1):
    print(f"Démarrage dans {i} secondes...")
    utime.sleep(2)

print("\nSysteme d'alarme actif !")
print("="*40)

derniere_touche = None
temps_derniere_touche = 0
distance_actuelle = 0

dernier_affichage_client = 0
delai_affichage = 2000     


while True:
    distance = distanceMax()

    if distance != -1:
        distance_actuelle = distance
        #print("Distance:", round(distance, 1), "cm")

        # --- Détection d'intrusion ---
        if distance < distance_max and not alarme_active:
            print("ALERTE ! Objet détecté !")
            color(1, 0, 0)       # LED rouge
            activer_buzzer()     # Buzzer ON
            alarme_active = True
            notification = True

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
            notification = False

    try:
        client, addr_client = s.accept()
        temps = utime.ticks_ms()
        if utime.ticks_diff(temps, dernier_affichage_client) > delai_affichage:
            print(f"Client connecté depuis {addr_client}")
            dernier_affichage_client = temps
        request = client.recv(1024)
        
        response = webpage(distance_actuelle, distance_max, alarme_active, len(code_saisi))
        http_response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n\r\n' + response
        client.send(http_response)
        client.close()

    except OSError:
        pass

    utime.sleep_ms(2)

