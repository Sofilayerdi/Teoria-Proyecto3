"""Estructura de la configuracion de la maquina de Turing."""

from __future__ import annotations 

from dataclasses import dataclass, field  
from typing import Iterable, List, Optional 

from .transition import Transition


def _copy_str_list(values: Iterable[str], field_name: str) -> list[str]:
    """
    Copia los valores en una lista nueva y valida que todos sean strings
    """
    copied = list(values)
    if not all(isinstance(v, str) for v in copied):
        raise ValueError(f"All values for '{field_name}' must be strings.")
    return copied


@dataclass(slots=True)
class MachineConfig:
    """
    Configuracion de una Maquina de Turing de una cinta.
    """

    states: List[str]                   # Lista de nombres de estados
    input_alphabet: List[str]           # Alfabeto de entrada (simbolos permitidos)
    tape_alphabet: List[str]            # Alfabeto de la cinta (incluye input_alphabet, extras y blank)
    initial_state: str                  # Estado inicial de la MT
    accept_states: List[str]            # Lista de estados de aceptacion
    transitions: List[Transition]       # Todas las transiciones de la MT
    inputs: Optional[List[str]] = None  # lista de cadenas a simular (YAML)
    blank_symbol: str = "B"             # Simbolo usado como blank

    def __post_init__(self) -> None:  
        """Normaliza y valida la configuracion"""

        # Normalizamos y clonamos la lista de estados
        self.states = _copy_str_list(self.states, "states")
        if not self.states:
            raise ValueError("Configuration must define at least one state.")

        # Normalizamos alfabetos
        self.input_alphabet = _copy_str_list(self.input_alphabet, "input_alphabet")
        self.tape_alphabet = _copy_str_list(self.tape_alphabet, "tape_alphabet")

        # input_alphabet debe ser subconjunto del alfabeto de la cinta
        if not set(self.input_alphabet).issubset(set(self.tape_alphabet)):
            raise ValueError("input_alphabet must be a subset of tape_alphabet.")

        # Normalizamos estados de aceptacion
        self.accept_states = _copy_str_list(self.accept_states, "accept_states")

        # Validamos estado inicial
        if not isinstance(self.initial_state, str) or self.initial_state == "":
            raise ValueError("initial_state must be a non-empty string.")
        if self.initial_state not in self.states:
            raise ValueError("initial_state must belong to states list.")

        # Validamos que todos los estados de aceptacion existan
        missing_accept = [s for s in self.accept_states if s not in self.states]
        if missing_accept:
            raise ValueError(f"accept_states {missing_accept} must belong to states list.")

        # Validamos que el simbolo blank exista en el alfabeto de cinta
        tape_symbols = set(self.tape_alphabet)
        if self.blank_symbol not in tape_symbols:
            raise ValueError("blank_symbol must be part of tape_alphabet.")

        # Normalizamos inputs
        if self.inputs is not None:
            self.inputs = _copy_str_list(self.inputs, "inputs")

        # Validamos transiciones
        if not isinstance(self.transitions, list) or not all(
            isinstance(t, Transition) for t in self.transitions
        ):
            raise ValueError("transitions must be a list of Transition objects.")
        if not self.transitions:
            raise ValueError("Configuration must contain at least one transition.")