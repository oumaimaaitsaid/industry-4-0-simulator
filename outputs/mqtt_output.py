"""
Module de publication MQTT
Cahier des charges Usine 4.0
"""

import json
import asyncio
from typing import Dict, Any
from .base_output import BaseOutput

# Simulation MQTT pour le développement
# En production, utilisez paho-mqtt
class MockMQTTClient:
    """Client MQTT simulé pour développement"""
    
    def __init__(self, broker_host: str, broker_port: int, username=None, password=None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.connected = False
    
    async def connect(self):
        """Simuler la connexion au broker MQTT"""
        await asyncio.sleep(0.1)  # Simuler délai de connexion
        self.connected = True
        return True
    
    async def publish(self, topic: str, payload: str, qos: int = 0):
        """Simuler la publication MQTT"""
        if not self.connected:
            raise Exception("Non connecté au broker MQTT")
        
        await asyncio.sleep(0.01)  # Simuler envoi
        return True
    
    async def disconnect(self):
        """Simuler la déconnexion"""
        self.connected = False

class MQTTOutput(BaseOutput):
    """Module de publication sur broker MQTT"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None
        self.broker_host = config.get('broker_host', 'localhost')
        self.broker_port = config.get('broker_port', 1883)
        self.topic = config.get('topic', 'usine/machine/data')
        self.qos = config.get('qos', 0)
        self.username = config.get('username')
        self.password = config.get('password')
    
    async def initialize(self):
        """Initialiser le client MQTT"""
        if self.enabled:
            try:
                self.client = MockMQTTClient(
                    self.broker_host,
                    self.broker_port,
                    self.username,
                    self.password
                )
                
                await self.client.connect()
                self.logger.info(f"MQTT connecté à {self.broker_host}:{self.broker_port}")
                print(f"📡 MQTT Output activé - {self.broker_host}:{self.broker_port}")
                
            except Exception as e:
                self.logger.error(f"Échec connexion MQTT: {e}")
                print(f"❌ MQTT: Connexion échouée")
                self.enabled = False
    
    async def send_data(self, data: Dict[str, Any]):
        """Publier les données sur le topic MQTT"""
        if not self.enabled or not self.client:
            return
        
        try:
            payload = json.dumps(data, ensure_ascii=False)
            await self.client.publish(self.topic, payload, self.qos)
            self.logger.debug(f"Données publiées sur {self.topic}")
            print(f"✅ MQTT: Publié sur {self.topic}")
            
        except Exception as e:
            self.logger.error(f"Erreur publication MQTT: {e}")
            print(f"❌ MQTT: Erreur - {e}")
    
    async def cleanup(self):
        """Fermer la connexion MQTT"""
        if self.client:
            await self.client.disconnect()
            print("📡 MQTT Output fermé")
            self.logger.info("Connexion MQTT fermée")