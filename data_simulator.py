"""
Générateur de données simulées pour automate industriel
Conforme au cahier des charges Usine 4.0
"""

import random
import time
import json
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataSimulator:
    """Générateur de données d'automate industriel"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.machine_config = config.get('machine', {})
        self.sensors_config = config.get('sensors', {})
        
        # États des capteurs
        self.sensor_states = self._init_sensors()
        
        logger.info("Simulateur de données initialisé")
    
    def _init_sensors(self) -> Dict[str, Any]:
        """Initialiser les états des capteurs"""
        return {
            'temperature': {
                'current': self.sensors_config.get('temperature', {}).get('initial', 25.0),
                'min': self.sensors_config.get('temperature', {}).get('min', 15.0),
                'max': self.sensors_config.get('temperature', {}).get('max', 85.0),
                'variation': self.sensors_config.get('temperature', {}).get('variation', 2.0)
            },
            'humidity': {
                'current': self.sensors_config.get('humidity', {}).get('initial', 50.0),
                'min': self.sensors_config.get('humidity', {}).get('min', 30.0),
                'max': self.sensors_config.get('humidity', {}).get('max', 90.0),
                'variation': self.sensors_config.get('humidity', {}).get('variation', 5.0)
            },
            'rpm': {
                'current': self.sensors_config.get('rpm', {}).get('initial', 1450),
                'min': self.sensors_config.get('rpm', {}).get('min', 0),
                'max': self.sensors_config.get('rpm', {}).get('max', 3000),
                'variation': self.sensors_config.get('rpm', {}).get('variation', 50)
            },
            'vibration': {
                'current': self.sensors_config.get('vibration', {}).get('initial', 1.0),
                'min': self.sensors_config.get('vibration', {}).get('min', 0.5),
                'max': self.sensors_config.get('vibration', {}).get('max', 5.0),
                'variation': self.sensors_config.get('vibration', {}).get('variation', 0.2)
            },
            'energy': {
                'current': self.sensors_config.get('energy', {}).get('initial', 2.5),
                'min': self.sensors_config.get('energy', {}).get('min', 0.5),
                'max': self.sensors_config.get('energy', {}).get('max', 15.0),
                'variation': self.sensors_config.get('energy', {}).get('variation', 0.5)
            },
            'uptime': {
                'start_time': time.time(),
                'total': 0
            },
            'status': {
                'current': 'ON',
                'states': ['ON', 'OFF', 'ERREUR']
            }
        }
    
    def _update_sensor(self, sensor_name: str) -> float:
        """Mettre à jour la valeur d'un capteur"""
        state = self.sensor_states[sensor_name]
        
        # Variation aléatoire
        variation = random.uniform(-state['variation'], state['variation'])
        new_value = state['current'] + variation
        
        # Limiter aux bornes min/max
        new_value = max(state['min'], min(state['max'], new_value))
        
        # Mettre à jour l'état
        state['current'] = new_value
        
        return new_value
    
 
