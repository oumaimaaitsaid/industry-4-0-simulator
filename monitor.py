"""
Script de monitoring du simulateur
"""

import json
import time
from pathlib import Path
from datetime import datetime

def monitor_data_file():
    """Surveiller le fichier de données"""
    data_file = Path("data/machine_data.json")
    
    if not data_file.exists():
        print("❌ Fichier de données introuvable")
        return
    
    print("📊 MONITORING DU SIMULATEUR")
    print("=" * 40)
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        if not data:
            print("❌ Aucune donnée trouvée")
            return
        
        # Statistiques
        total_records = len(data)
        latest_record = data[-1]
        
        print(f"📈 Total d'enregistrements: {total_records}")
        print(f"🕐 Dernier timestamp: {latest_record['timestamp']}")
        print(f"🏭 Machine ID: {latest_record['machine_id']}")
        print(f"🌡️  Température: {latest_record['temperature']}°C")
        print(f"💧 Humidité: {latest_record['humidity']}%")
        print(f"⚙️  RPM: {latest_record['rpm']}")
        print(f"📳 Vibration: {latest_record['vibration']}mm/s")
        print(f"⚡ Énergie: {latest_record['energy_kwh']}kWh")
        print(f"⏱️  Uptime: {latest_record['uptime']}s")
        print(f"🔄 Statut: {latest_record['status']}")
        
        # Calculs statistiques
        if total_records > 1:
            temps = [record['temperature'] for record in data]
            temp_avg = sum(temps) / len(temps)
            temp_min = min(temps)
            temp_max = max(temps)
            
            print("\n📊 STATISTIQUES TEMPÉRATURE:")
            print(f"   Moyenne: {temp_avg:.1f}°C")
            print(f"   Minimum: {temp_min:.1f}°C")
            print(f"   Maximum: {temp_max:.1f}°C")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    monitor_data_file()