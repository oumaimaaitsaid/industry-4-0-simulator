
"""
Simulateur Python pour Usine 4.0
Script principal selon le cahier des charges
"""

import asyncio
import yaml
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path


from data_simulator import DataSimulator
from outputs.console_output import ConsoleOutput
from outputs.http_output import HTTPOutput
from outputs.mqtt_output import MQTTOutput
from outputs.file_output import FileOutput

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimulateurUsine:
    """Simulateur principal pour Usine 4.0"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.data_simulator = DataSimulator(self.config)
        self.outputs = []
        self.running = False
        
        # Initialiser les modules de sortie
        self._initialize_outputs()
        
        # Gestionnaire de signaux pour arrêt propre
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self):
        """Charger la configuration depuis config.yaml"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            logger.info(f"Configuration chargée depuis {self.config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Fichier de configuration {self.config_path} introuvable")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Erreur dans le fichier YAML: {e}")
            sys.exit(1)
    
