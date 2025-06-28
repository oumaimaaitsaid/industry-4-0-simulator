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

    
