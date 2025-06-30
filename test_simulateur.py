"""
Tests unitaires pour le Simulateur Usine 4.0
Conforme au cahier des charges
"""

import unittest
import asyncio
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import des modules à tester
from data_simulator import DataSimulator
from outputs.console_output import ConsoleOutput
from outputs.file_output import FileOutput
from outputs.http_output import HTTPOutput

class TestDataSimulator(unittest.TestCase):
    """Tests pour le générateur de données"""
    
    def setUp(self):
        """Configuration de test"""
        self.test_config = {
            'machine': {
                'id': 'TEST-01',
                'name': 'Machine de test'
            },
            'sensors': {
                'temperature': {'initial': 25.0, 'min': 15.0, 'max': 85.0, 'variation': 2.0},
                'humidity': {'initial': 50.0, 'min': 30.0, 'max': 90.0, 'variation': 5.0},
                'rpm': {'initial': 1450, 'min': 0, 'max': 3000, 'variation': 50},
                'vibration': {'initial': 1.0, 'min': 0.5, 'max': 5.0, 'variation': 0.2},
                'energy': {'initial': 2.5, 'min': 0.5, 'max': 15.0, 'variation': 0.5}
            }
        }
        self.simulator = DataSimulator(self.test_config)
    
    def test_data_generation_format(self):
        """Test: Format des données généré"""
        data = self.simulator.generate_data()
        
        # Vérifier les champs obligatoires du cahier des charges
        required_fields = [
            'timestamp', 'machine_id', 'temperature', 'humidity',
            'rpm', 'vibration', 'energy_kwh', 'uptime', 'status'
        ]
        
        for field in required_fields:
            self.assertIn(field, data, f"Champ manquant: {field}")
        
        print("✅ Test format des données: RÉUSSI")
    
    def test_data_types(self):
        """Test: Types de données corrects"""
        data = self.simulator.generate_data()
        
        # Vérifier les types selon le cahier des charges
        self.assertIsInstance(data['timestamp'], str)
        self.assertIsInstance(data['machine_id'], str)
        self.assertIsInstance(data['temperature'], (int, float))
        self.assertIsInstance(data['humidity'], (int, float))
        self.assertIsInstance(data['rpm'], int)
        self.assertIsInstance(data['vibration'], (int, float))
        self.assertIsInstance(data['energy_kwh'], (int, float))
        self.assertIsInstance(data['uptime'], int)
        self.assertIsInstance(data['status'], str)
        
        print("✅ Test types de données: RÉUSSI")
    
    def test_sensor_bounds(self):
        """Test: Limites des capteurs respectées"""
        # Générer plusieurs échantillons
        for i in range(50):
            data = self.simulator.generate_data()
            
            # Vérifier les limites
            self.assertGreaterEqual(data['temperature'], 15.0)
            self.assertLessEqual(data['temperature'], 85.0)
            
            self.assertGreaterEqual(data['humidity'], 30.0)
            self.assertLessEqual(data['humidity'], 90.0)
            
            self.assertGreaterEqual(data['rpm'], 0)
            self.assertLessEqual(data['rpm'], 3000)
            
            self.assertGreaterEqual(data['vibration'], 0.5)
            self.assertLessEqual(data['vibration'], 5.0)
            
            self.assertGreaterEqual(data['energy_kwh'], 0.5)
            self.assertLessEqual(data['energy_kwh'], 15.0)
        
        print("✅ Test limites capteurs: RÉUSSI")
    
    def test_machine_status(self):
        """Test: États de machine valides"""
        valid_statuses = ['ON', 'OFF', 'ERREUR']
        
        for _ in range(20):
            data = self.simulator.generate_data()
            self.assertIn(data['status'], valid_statuses)
        
        print("✅ Test états machine: RÉUSSI")

class TestOutputs(unittest.TestCase):
    """Tests pour les modules de sortie"""
    
    def setUp(self):
        """Données de test"""
        self.test_data = {
            'timestamp': '2025-06-28T10:00:00Z',
            'machine_id': 'TEST-01',
            'temperature': 25.5,
            'humidity': 60.0,
            'rpm': 1500,
            'vibration': 1.2,
            'energy_kwh': 3.0,
            'uptime': 3600,
            'status': 'ON'
        }
    
    def test_console_output(self):
        """Test: Sortie console"""
        config = {'enabled': True, 'format': 'simple'}
        console = ConsoleOutput(config)
        
        # Capturer la sortie
        with patch('builtins.print') as mock_print:
            asyncio.run(console.send_data(self.test_data))
            mock_print.assert_called()
        
        print("✅ Test console output: RÉUSSI")
    
    def test_file_output_json(self):
        """Test: Sauvegarde fichier JSON"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {
                'enabled': True,
                'path': f"{temp_dir}/test_output.json",
                'format': 'json',
                'rotation': False
            }
            
            file_output = FileOutput(config)
            
            # Test sauvegarde
            asyncio.run(file_output.initialize())
            asyncio.run(file_output.send_data(self.test_data))
            asyncio.run(file_output.cleanup())
            
            # Vérifier fichier créé
            output_file = Path(config['path'])
            self.assertTrue(output_file.exists())
            
            # Vérifier contenu
            with open(output_file, 'r') as f:
                saved_data = json.load(f)
                self.assertIsInstance(saved_data, list)
                self.assertEqual(len(saved_data), 1)
                self.assertEqual(saved_data[0]['machine_id'], 'TEST-01')
        
        print("✅ Test file output JSON: RÉUSSI")
    
    def test_file_output_csv(self):
        """Test: Sauvegarde fichier CSV"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {
                'enabled': True,
                'path': f"{temp_dir}/test_output.csv",
                'format': 'csv',
                'rotation': False
            }
            
            file_output = FileOutput(config)
            
            # Test sauvegarde
            asyncio.run(file_output.initialize())
            asyncio.run(file_output.send_data(self.test_data))
            asyncio.run(file_output.cleanup())
            
            # Vérifier fichier créé
            output_file = Path(config['path'])
            self.assertTrue(output_file.exists())
            
            # Vérifier contenu CSV
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertIn('timestamp,machine_id', content)  # En-têtes
                self.assertIn('TEST-01', content)  # Données
        
        print("✅ Test file output CSV: RÉUSSI")

class TestPerformance(unittest.TestCase):
    """Tests de performance selon cahier des charges"""
    
    def test_10_machines_5_seconds(self):
        """Test: 10 machines / envoi toutes les 5 sec"""
        import time
        
        # Configuration pour 10 machines
        configs = []
        simulators = []
        
        for i in range(10):
            config = {
                'machine': {'id': f'AUTO-{i:02d}', 'name': f'Machine {i}'},
                'sensors': {
                    'temperature': {'initial': 25.0, 'min': 15.0, 'max': 85.0, 'variation': 2.0},
                    'humidity': {'initial': 50.0, 'min': 30.0, 'max': 90.0, 'variation': 5.0},
                    'rpm': {'initial': 1450, 'min': 0, 'max': 3000, 'variation': 50},
                    'vibration': {'initial': 1.0, 'min': 0.5, 'max': 5.0, 'variation': 0.2},
                    'energy': {'initial': 2.5, 'min': 0.5, 'max': 15.0, 'variation': 0.5}
                }
            }
            simulators.append(DataSimulator(config))
        
        # Test génération rapide
        start_time = time.time()
        
        for _ in range(3):  # 3 cycles de 5 secondes
            for simulator in simulators:
                data = simulator.generate_data()
                self.assertIsNotNone(data)
            time.sleep(0.1)  # Simuler traitement
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Doit être rapide (moins de 2 secondes pour 30 générations)
        self.assertLess(total_time, 2.0)
        
        print(f"✅ Test performance 10 machines: RÉUSSI ({total_time:.2f}s)")

def run_all_tests():
    """Exécuter tous les tests"""
    print("🧪 DÉBUT DES TESTS UNITAIRES")
    print("=" * 50)
    
    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter les tests
    suite.addTests(loader.loadTestsFromTestCase(TestDataSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestOutputs))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 50)
    if result.wasSuccessful():
        print("🎉 TOUS LES TESTS RÉUSSIS!")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print(f"Échecs: {len(result.failures)}")
        print(f"Erreurs: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_all_tests()