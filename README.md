# Système d'Alarme Intelligent - Raspberry Pi Pico

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Pico%20W-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)
![MicroPython](https://img.shields.io/badge/MicroPython-2B2728?style=for-the-badge&logo=micropython&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-System-blue?style=for-the-badge&logo=homeassistant&logoColor=white)

## 📝 Description du Projet

Ce projet consiste en la création d'un système d'alarme intelligent et connecté, développé pour Raspberry Pi Pico W. Le système utilise un capteur à ultrasons pour détecter les intrusions, déclenche une alarme sonore et lumineuse, et peut être désactivé via un code PIN saisi sur un clavier matriciel. Une interface web permet également de surveiller l'état de l'alarme à distance via WiFi.

> **ℹ️ Note importante** : Ce README et le code du programme seront traduits en anglais le **16 ou 17 janvier 2026**.

## ✨ Fonctionnalités

- **Détection automatique d'intrusion** par capteur ultrason HC-SR04
- **Alarme multi-sensorielle** : buzzer piézoélectrique + LED RGB
- **Authentification sécurisée** via code PIN à 4 chiffres sur clavier matriciel 4x4
- **Interface web en temps réel** pour monitoring à distance
- **Indicateurs visuels** : LED verte (veille), LED rouge (alarme active)
- **Anti-rebond logiciel** pour éviter les saisies multiples
- **Système de timeout** pour le capteur ultrason

## 🛠️ Technologies Utilisées

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| **MicroPython** | Latest | Firmware et langage de programmation |
| **Raspberry Pi Pico W** | - | Microcontrôleur avec WiFi intégré |
| **HTML** | 5 | Interface web de monitoring |

### Composants Matériels

- **HC-SR04** - Capteur à ultrasons (détection 2-400 cm)
- **Clavier matriciel 4x4** - Saisie du code PIN
- **LED RGB** - Indicateurs visuels d'état
- **Buzzer piézoélectrique** - Alarme sonore

### Protocoles et APIs MicroPython

- **GPIO (General Purpose Input/Output)** - Communication avec composants électroniques
- **PWM (Pulse Width Modulation)** - Contrôle de l'intensité (buzzer, LEDs)
- **Socket API** - Serveur HTTP pour interface web
- **WLAN** - Connexion WiFi 802.11 b/g/n (2.4 GHz)

### Bibliothèques Utilisées

```python
from machine import Pin, PWM  # Contrôle GPIO et PWM
import utime                   # Gestion temporelle
import network                 # Connexion WiFi
import socket                  # Serveur web HTTP
```

## 📌 Schéma de Branchement

### Capteur Ultrason HC-SR04
- **Trigger** → GPIO 2
- **Echo** → GPIO 3
- **VCC** → 5V
- **GND** → GND

### Buzzer Piézoélectrique
- **Signal** → GPIO 15
- **GND** → GND

### LED RGB
- **Rouge** → GPIO 16
- **Vert** → GPIO 17
- **Bleu** → GPIO 18
- **GND/VCC** → GND/3.3V (selon type)

### Clavier Matriciel 4x4

**Lignes (Rows)**
- Ligne 1 → GPIO 6
- Ligne 2 → GPIO 7
- Ligne 3 → GPIO 8
- Ligne 4 → GPIO 9

**Colonnes (Cols)**
- Colonne 1 → GPIO 10
- Colonne 2 → GPIO 11
- Colonne 3 → GPIO 12
- Colonne 4 → GPIO 13

## 🚀 Installation et Lancement

### Prérequis

- Raspberry Pi Pico W
- MicroPython installé sur le Pico
- IDE compatible (Thonny, VS Code avec extension Pico, etc.)
- Tous les composants électroniques listés

### Étapes d'installation

```bash
# Cloner le repository
git clone git@github.com:Ne0xa/Motion-Guardian.git

# Naviguer vers le dossier du projet
cd Motion-Guardian
```

### Configuration

1. Ouvrir le fichier principal dans votre éditeur
2. Modifier les paramètres de configuration :

```python
# Code PIN (par défaut : 2704)
CODE_CORRECT = "2704"

# Distance de détection en cm
distance_max = 20

# Identifiants WiFi
ssid = "VOTRE_NOM_WIFI"
password = "VOTRE_MOT_DE_PASSE_WIFI"
```

### Lancement

1. Connecter tous les composants selon le schéma de branchement
2. Téléverser le code sur votre Raspberry Pi Pico W
3. Ouvrir le moniteur série pour voir l'adresse IP
4. Le système démarre automatiquement

## 💡 Utilisation

### Fonctionnement Normal

1. **Mode veille** : LED verte allumée, système en attente
2. **Détection d'intrusion** : 
   - Objet détecté à moins de 20 cm
   - LED devient rouge
   - Buzzer se déclenche
3. **Désactivation** :
   - Saisir le code PIN sur le clavier
   - Appuyer sur `#` pour valider (ou laisser valider automatiquement après 4 chiffres)
   - Appuyer sur `*` pour effacer

### Interface Web

Une fois connecté au WiFi, accédez à l'adresse IP affichée dans la console :
```
http://[ADRESSE_IP_DU_PICO]
```

L'interface affiche l'état actuel de l'alarme (ON/OFF).

## 🎯 Caractéristiques Techniques

- **Fréquence PWM** : 1000 Hz (buzzer et LEDs)
- **Résolution PWM** : 16 bits (0-65535)
- **Rafraîchissement** : 100 ms (10 Hz)
- **Timeout capteur** : 30 ms
- **Anti-rebond clavier** : 300 ms
- **Port serveur web** : 80 (HTTP)
- **Portée capteur** : 2-400 cm
- **Distance de détection** : Configurable (défaut 20 cm)

## 🔐 Sécurité

- ✅ Code PIN à 4 chiffres
- ✅ Affichage masqué du code (caractères remplacés par `*`)
- ✅ Réinitialisation automatique après validation
- ✅ Anti-rebond pour éviter les saisies multiples

⚠️ **Important** : Changez le code PIN par défaut (`2704`) avant utilisation en production

## 🛠️ Personnalisation

### Modifier la Distance de Détection
```python
distance_max = 30  # Détection à 30 cm au lieu de 20 cm
```

### Changer le Code PIN
```python
CODE_CORRECT = "1234"  # Votre code personnalisé
```

### Ajuster la Fréquence du Buzzer
```python
buzzer.freq(2000)  # Fréquence de 2000 Hz (son plus aigu)
```

### Personnaliser les Couleurs LED
```python
def color(r, g, b):
    red.duty_u16(int(65535 * r))    # Intensité variable (0.0 à 1.0)
    green.duty_u16(int(65535 * g))
    blue.duty_u16(int(65535 * b))
```

## 🐛 Dépannage

| Problème | Solution |
|----------|----------|
| **Capteur ne détecte rien** | Vérifier connexions Trigger/Echo et alimentation 5V |
| **WiFi ne se connecte pas** | Vérifier SSID/mot de passe et réseau en 2.4 GHz uniquement |
| **Clavier ne répond pas** | Vérifier toutes les connexions lignes/colonnes |
| **Buzzer silencieux** | Vérifier connexion GPIO 15 et polarité |
| **LED ne s'allume pas** | Vérifier type LED (anode/cathode commune) et connexions |
| **Erreur timeout capteur** | Réduire timeout ou vérifier obstacles devant capteur |

## 📊 Structure du Code

```
├── Initialisation GPIO
│   ├── Capteur ultrason (Trigger, Echo)
│   ├── Buzzer (PWM)
│   ├── LED RGB (PWM)
│   └── Clavier matriciel (4x4)
│
├── Fonctions principales
│   ├── distanceMax() - Mesure distance ultrason
│   ├── digiCode() - Lecture clavier matriciel
│   ├── verifCode() - Vérification code PIN
│   ├── gereTouche() - Gestion saisie clavier
│   └── color() - Contrôle LED RGB
│
├── Boucle principale
│   ├── Mesure distance
│   ├── Détection intrusion
│   ├── Gestion alarme
│   └── Saisie code PIN
│
└── Serveur Web
    ├── Connexion WiFi
    └── Page HTML status
```

## 📚 Ressources

- [Documentation MicroPython](https://docs.micropython.org/)
- [Raspberry Pi Pico W Datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf)
- [HC-SR04 Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)

## 👨‍🎓 Contexte Académique

**Cours**: Développement Web Front-End  
**Niveau**: [Première année bachelor]  
**Établissement**: [IIM-Digital School]  
**Semestre**: [B1]

## 📄 Licence

Ce projet est développé dans un cadre académique. Tous droits réservés à l'étudiant.
