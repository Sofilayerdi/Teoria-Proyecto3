"""clases principales de la Maquina de Turing de una cinta."""

from .instant_description import InstantDescription  # Estructura para snapshots (IDs)
from .machine import Machine                         # simulador
from .machine_config import MachineConfig            # Configuracion de la MT
from .state import State                             # Clase de estados
from .transition import Transition                   # Transiciones que definen la logica

__all__ = [
    "InstantDescription",
    "Machine",
    "MachineConfig",
    "State",
    "Transition",
]