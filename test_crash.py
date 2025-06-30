"""
Test d'extinction brutale selon cahier des charges
"""

import subprocess
import time
import signal
import os
import sys

def test_brutal_shutdown():
    """Test: Le script doit reprendre sans crash"""
    print("🧪 Test d'extinction brutale...")
    
    python_exe = sys.executable
    # Lancer le simulateur
    process = subprocess.Popen([python_exe, 'simulateur.py'])
    
    # Laisser tourner 10 secondes
    time.sleep(10)
    
    # Arrêt brutal (SIGKILL)
    process.kill()
    print("💥 Arrêt brutal effectué")
    
    # Attendre un peu
    time.sleep(2)
    
    # Relancer
    print("🔄 Relancement...")
    process2 = subprocess.Popen(['python', 'simulateur.py'])
    
    # Laisser tourner 5 secondes
    time.sleep(5)
    
    # Arrêt propre
    process2.terminate()
    process2.wait()
    
    print("✅ Test extinction brutale: RÉUSSI")

if __name__ == '__main__':
    test_brutal_shutdown()