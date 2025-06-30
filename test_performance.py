"""
Test de performance du simulateur industriel
"""

import time
import threading
from data_simulator import DataSimulator
import yaml

def test_single_machine():
    """Test performance machine unique"""
    print("🧪 Test performance - Machine unique")
    
    # Charger config
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    simulator = DataSimulator(config)
    
    # Test 100 générations
    start_time = time.time()
    
    for i in range(100):
        data = simulator.generate_data()
        if i % 20 == 0:
            print(f"  Génération {i+1}/100 - Temp: {data['temperature']}°C")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ 100 générations en {duration:.3f}s")
    print(f"📊 Performance: {100/duration:.1f} générations/seconde")

def test_multiple_machines():
    """Test performance multiples machines"""
    print("\n🏭 Test performance - 5 machines simultanées")
    
    def run_machine(machine_id):
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['machine']['id'] = f"AUTO-{machine_id:02d}"
        simulator = DataSimulator(config)
        
        for i in range(20):
            data = simulator.generate_data()
            time.sleep(0.1)  # Simulation 10 fois par seconde
        
        print(f"  ✅ Machine {machine_id} terminée")
    
    # Lancer 5 machines en parallèle
    start_time = time.time()
    threads = []
    
    for i in range(1, 6):
        thread = threading.Thread(target=run_machine, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Attendre toutes les machines
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ 5 machines terminées en {duration:.3f}s")

def test_memory_usage():
    """Test utilisation mémoire"""
    print("\n💾 Test utilisation mémoire")
    
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    simulators = []
    
    # Créer 10 simulateurs
    for i in range(10):
        config['machine']['id'] = f"MEM-{i:02d}"
        simulator = DataSimulator(config)
        simulators.append(simulator)
    
    print(f"✅ {len(simulators)} simulateurs créés en mémoire")
    
    # Générer données pour tous
    total_data = []
    for simulator in simulators:
        for _ in range(10):
            data = simulator.generate_data()
            total_data.append(data)
    
    print(f"📊 {len(total_data)} échantillons générés")
    print(f"💾 Taille approximative: {len(str(total_data))} caractères")

if __name__ == '__main__':
    print("🚀 TESTS DE PERFORMANCE - SIMULATEUR USINE 4.0")
    print("=" * 60)
    
    try:
        test_single_machine()
        test_multiple_machines()
        test_memory_usage()
        
        print("\n🎉 TOUS LES TESTS DE PERFORMANCE RÉUSSIS!")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("Vérifiez que data_simulator.py et config.yaml existent")