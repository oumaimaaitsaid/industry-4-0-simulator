"""
Module d'affichage console
Cahier des charges Usine 4.0
"""

import json
from typing import Dict, Any
from .base_output import BaseOutput

class ConsoleOutput(BaseOutput):
    """Module d'affichage à l'écran pour test"""
    
    async def initialize(self):
        """Initialiser l'affichage console"""
        if self.enabled:
            self.logger.info("Module console initialisé")
            print("🖥️  Console Output activé")
    
    async def send_data(self, data: Dict[str, Any]):
        """Afficher les données à l'écran"""
        if not self.enabled:
            return
        
        try:
            format_type = self.config.get('format', 'simple')
            
            if format_type == 'detailed':
                # Format détaillé JSON
                print("\n" + "="*60)
                print("📊 DONNÉES MACHINE")
                print("="*60)
                print(json.dumps(data, indent=2, ensure_ascii=False))
                print("="*60)
            else:
                # Format simple sur une ligne
                print(f"[{data['timestamp']}] "
                      f"Machine: {data['machine_id']} | "
                      f"Temp: {data['temperature']}°C | "
                      f"Humidité: {data['humidity']}% | "
                      f"RPM: {data['rpm']} | "
                      f"Vibration: {data['vibration']}mm/s | "
                      f"Énergie: {data['energy_kwh']}kWh | "
                      f"Uptime: {data['uptime']}s | "
                      f"Statut: {data['status']}")
            
        except Exception as e:
            self.logger.error(f"Erreur affichage console: {e}")
    
    async def cleanup(self):
        """Nettoyer l'affichage console"""
        if self.enabled:
            print("\n🛑 Console Output fermé")
            self.logger.info("Module console fermé")