
# Simulateur Python pour Usine 4.0

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)


## 📋 Description

Simulateur modulaire Python développé selon le cahier des charges Usine 4.0. Il génère des données d'automatisation industrielle réalistes et les envoie vers différents backends (HTTP API, MQTT Broker, fichiers, etc.).

## 🚀 Fonctionnalités

### Génération dynamique des données
- **Température** (°C) - Plage configurable 15-85°C
- **Humidité relative** (%) - Variation réaliste 30-90%
- **Vitesse de rotation** (RPM) - Simulation moteur 0-3000
- **Vibrations** (mm/s) - Détection d'anomalies 0.5-5.0
- **Consommation électrique** (kWh) - Monitoring énergétique
- **Temps de fonctionnement** (Uptime) - Disponibilité machine
- **État de la machine** (ON, OFF, ERREUR) - Statut opérationnel

### Modularité des sorties
- 🖥️ **Console** : Affichage temps réel
- 🌐 **HTTP** : Envoi vers API REST
- 📡 **MQTT** : Publication sur broker IoT
- 💾 **File** : Sauvegarde locale (JSON/CSV)

## 📦 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation rapide

```bash
# 1. Cloner le projet
git clone https://github.com/oumaimaaitsaid/industry-4-0-simulator.git
cd simulateur-usine-4-0

# 2. Créer environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

## Configuration

Le fichier `config.yaml` permet de configurer tous les paramètres :

```yaml
# Configuration machine
machine:
  id: "AUTO-01"
  name: "Ligne de production Alpha"
  location: "Atelier 1"

# Paramètres simulation
simulation:
  interval: 5  # secondes entre envois
  duration: 0  # 0 = infini

# Sorties activées
outputs:
  console:
    enabled: true
  file:
    enabled: true
    path: "data/machine_data.json"
  http:
    enabled: false
    url: "http://your-api.com/data"
  mqtt:
    enabled: false
    broker_host: "localhost"
```

## Utilisation

### Démarrage basique

```shellscript
python simulateur.py
```

### Avec fichier de configuration personnalisé

```shellscript
python simulateur.py ma_config.yaml
```

### Arrêt propre

```shellscript
# Ctrl+C pour arrêt gracieux
# Le simulateur sauvegarde et ferme proprement toutes les connexions
```

## Format des données

Les données générées respectent le format JSON spécifié :

```json
{
  "timestamp": "2025-06-28T10:15:30Z",
  "machine_id": "AUTO-01",
  "temperature": 68.2,
  "humidity": 50.3,
  "rpm": 1450,
  "vibration": 1.1,
  "energy_kwh": 2.8,
  "uptime": 157000,
  "status": "ON"
}
```

## Tests

### Tests unitaires

```shellscript
python test_simulateur.py
```

### Test de performance

```shellscript
python test_performance.py
```

### Test de robustesse

```shellscript
python test_crash.py
```

### Monitoring en temps réel

```shellscript
python monitor.py
```

## Structure du projet

```plaintext
simulateur_usine/
├── simulateur.py          # Script principal
├── config.yaml           # Configuration utilisateur
├── data_simulator.py     # Génération données simulées
├── outputs/
│   ├── base_output.py    # Interface commune
│   ├── console_output.py # Affichage console
│   ├── http_output.py    # Envoi HTTP
│   ├── mqtt_output.py    # Publication MQTT
│   └── file_output.py    # Sauvegarde fichier
├── test_simulateur.py    # Tests unitaires
├── test_performance.py   # Tests de performance
├── test_crash.py         # Tests de robustesse
├── monitor.py            # Monitoring temps réel
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
├── data/                # Données générées
└── logs/                # Fichiers de log
```

## Extensibilité

### Ajouter un nouveau capteur

1. **Modifier `data_simulator.py`** :


```python
# Ajouter dans _init_sensors()
'pression': {
    'current': 1.0,
    'min': 0.5,
    'max': 2.0,
    'variation': 0.1
}
```

2. **Mettre à jour `config.yaml`** :


```yaml
sensors:
  pression:
    initial: 1.0
    min: 0.5
    max: 2.0
    variation: 0.1
```

### Ajouter un module de sortie

1. **Créer `outputs/nouveau_output.py`** héritant de `BaseOutput`
2. **Intégrer dans `simulateur.py`**


## Performance

### Benchmarks validés

- ✅ **10 machines simultanées** - Génération stable
- ✅ **Envoi toutes les 5 secondes** - Fonctionnement 24h/24
- ✅ **Extinction brutale** - Reprise sans corruption
- ✅ **Gestion mémoire** - Optimisée pour production


## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request


## Licence

Ce projet est développé dans le cadre du cours Usine 4.0.

## Auteur

- **OUMAIMA AIT SAID** - Développement complet


---

**Simulateur Usine 4.0** - Générer l'avenir industriel 🏭

