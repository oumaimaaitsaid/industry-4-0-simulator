"""
Module d'enregistrement dans fichier local
Cahier des charges Usine 4.0
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from .base_output import BaseOutput

class FileOutput(BaseOutput):
    """Module de sauvegarde dans fichier local (JSON ou CSV)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.file_path = Path(config.get('path', 'data/machine_data.json'))
        self.format = config.get('format', 'json').lower()
        self.rotation = config.get('rotation', False)
        self.max_size_mb = config.get('max_size_mb', 10)
        
        # Créer le dossier si nécessaire
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """Initialiser l'enregistrement fichier"""
        if self.enabled:
            self.logger.info(f"Module fichier initialisé - {self.file_path}")
            print(f"💾 File Output activé - {self.file_path}")
            
            # Créer fichier CSV avec en-têtes si nécessaire
            if self.format == 'csv' and not self.file_path.exists():
                await self._create_csv_headers()
    
    async def send_data(self, data: Dict[str, Any]):
        """Sauvegarder les données dans le fichier"""
        if not self.enabled:
            return
        
        try:
            # Vérifier rotation si activée
            if self.rotation and self._should_rotate():
                self._rotate_file()
            
            # Sauvegarder selon le format
            if self.format == 'json':
                await self._save_json(data)
            elif self.format == 'csv':
                await self._save_csv(data)
            else:
                self.logger.error(f"Format non supporté: {self.format}")
                return
            
            print(f"✅ File: Sauvegardé ({self.format.upper()})")
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde fichier: {e}")
            print(f"❌ File: Erreur - {e}")
    
    async def _save_json(self, data: Dict[str, Any]):
        """Sauvegarder en format JSON"""
        # Lire données existantes
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
            except (json.JSONDecodeError, Exception):
                existing_data = []
        else:
            existing_data = []
        
        # Ajouter nouvelles données
        existing_data.append(data)
        
        # Sauvegarder
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    async def _save_csv(self, data: Dict[str, Any]):
        """Sauvegarder en format CSV"""
        file_exists = self.file_path.exists()
        
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            
            # Écrire en-têtes si nouveau fichier
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data)
    
    async def _create_csv_headers(self):
        """Créer fichier CSV avec en-têtes"""
        headers = [
            'timestamp', 'machine_id', 'temperature', 'humidity', 
            'rpm', 'vibration', 'energy_kwh', 'uptime', 'status'
        ]
        
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    
    def _should_rotate(self) -> bool:
        """Vérifier si rotation nécessaire"""
        if not self.file_path.exists():
            return False
        
        size_mb = self.file_path.stat().st_size / (1024 * 1024)
        return size_mb > self.max_size_mb
    
    def _rotate_file(self):
        """Effectuer la rotation du fichier"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rotated_name = f"{self.file_path.stem}_{timestamp}{self.file_path.suffix}"
        rotated_path = self.file_path.parent / rotated_name
        
        self.file_path.rename(rotated_path)
        self.logger.info(f"Fichier pivoté vers: {rotated_path}")
        print(f"🔄 File: Rotation vers {rotated_name}")
    
    async def cleanup(self):
        """Nettoyer le module fichier"""
        if self.enabled:
            print("💾 File Output fermé")
            self.logger.info("Module fichier fermé")