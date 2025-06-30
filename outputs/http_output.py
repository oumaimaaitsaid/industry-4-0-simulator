"""
Module d'envoi HTTP vers API REST
Cahier des charges Usine 4.0
"""

import json
import aiohttp
from typing import Dict, Any
from .base_output import BaseOutput

class HTTPOutput(BaseOutput):
    """Module d'envoi vers API REST"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.session = None
        self.url = config.get('url', 'http://localhost:8080/api/data')
        self.headers = config.get('headers', {'Content-Type': 'application/json'})
        self.timeout = config.get('timeout', 10)
    
    async def initialize(self):
        """Initialiser la session HTTP"""
        if self.enabled:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self.headers
            )
            self.logger.info(f"Module HTTP initialisé - URL: {self.url}")
            print(f"🌐 HTTP Output activé - {self.url}")
    
    async def send_data(self, data: Dict[str, Any]):
        """Envoyer les données via HTTP POST"""
        if not self.enabled or not self.session:
            return
        
        try:
            async with self.session.post(self.url, json=data) as response:
                if response.status == 200:
                    self.logger.debug(f"Données envoyées avec succès à {self.url}")
                    print(f"✅ HTTP: Données envoyées ({response.status})")
                else:
                    self.logger.warning(f"Échec HTTP: statut {response.status}")
                    print(f"⚠️  HTTP: Échec ({response.status})")
                    
        except aiohttp.ClientError as e:
            self.logger.error(f"Erreur client HTTP: {e}")
            print(f"❌ HTTP: Erreur de connexion")
        except Exception as e:
            self.logger.error(f"Erreur HTTP: {e}")
            print(f"❌ HTTP: Erreur - {e}")
    
    async def cleanup(self):
        """Fermer la session HTTP"""
        if self.session:
            await self.session.close()
            print("🌐 HTTP Output fermé")
            self.logger.info("Session HTTP fermée")