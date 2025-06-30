
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

