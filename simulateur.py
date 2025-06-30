
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
    
    def _initialize_outputs(self):
        """Initialiser les modules de sortie selon la configuration"""
        outputs_config = self.config.get('outputs', {})
        
        # Console output
        if outputs_config.get('console', {}).get('enabled', False):
            self.outputs.append(ConsoleOutput(outputs_config['console']))
        
        # HTTP output
        if outputs_config.get('http', {}).get('enabled', False):
            self.outputs.append(HTTPOutput(outputs_config['http']))
        
        # MQTT output
        if outputs_config.get('mqtt', {}).get('enabled', False):
            self.outputs.append(MQTTOutput(outputs_config['mqtt']))
        
        # File output
        if outputs_config.get('file', {}).get('enabled', False):
            self.outputs.append(FileOutput(outputs_config['file']))
        
        logger.info(f"Initialisé {len(self.outputs)} modules de sortie")
    
    def _signal_handler(self, signum, frame):
        """Gestionnaire d'arrêt propre"""
        logger.info(f"Signal {signum} reçu, arrêt en cours...")
        self.running = False
    
    async def run(self):
        """Boucle principale du simulateur"""
        logger.info("🏭 Démarrage du Simulateur Usine 4.0")
        self.running = True
        
        # Initialiser tous les outputs
        for output in self.outputs:
            await output.initialize()
        
        try:
            interval = self.config.get('simulation', {}).get('interval', 5)
            
            while self.running:
                # Générer les données
                data = self.data_simulator.generate_data()
                
                # Envoyer vers tous les outputs
                tasks = []
                for output in self.outputs:
                    tasks.append(output.send_data(data))
                
                # Attendre que tous les envois se terminent
                await asyncio.gather(*tasks, return_exceptions=True)
                
                # Attendre l'intervalle configuré
                await asyncio.sleep(interval)
                
        except Exception as e:
            logger.error(f"Erreur dans la boucle principale: {e}")
        finally:
            # Nettoyage
            for output in self.outputs:
                await output.cleanup()
            
            logger.info("Simulateur arrêté proprement")

