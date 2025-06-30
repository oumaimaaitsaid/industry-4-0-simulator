"""
Interface commune pour tous les modules de sortie
Cahier des charges Usine 4.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseOutput(ABC):
    """Classe abstraite pour tous les modules de sortie"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', False)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def initialize(self):
        """Initialiser le module de sortie"""
        pass
    
    @abstractmethod
    async def send_data(self, data: Dict[str, Any]):
        """Envoyer les données via ce module"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Nettoyer les ressources"""
        pass