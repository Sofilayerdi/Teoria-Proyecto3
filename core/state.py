"""Definicion de estados de la Maquina de Turing."""

from __future__ import annotations  

from dataclasses import dataclass 


@dataclass(frozen=True, slots=True)
class State:
    """
    Representa un unico estado de la maquina.

    Nota: esta clase existe para ser claros en la representacion de los componentes de la maquina.
    """

    name: str  # Nombre del estado, por ejemplo "q0", "q1"

    def __post_init__(self) -> None: 
        """Validamos que el nombre del estado sea un string no vacio."""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("State name must be a non-empty string.")

    def __str__(self) -> str:
        """Cuando convertimos el estado a string, devolvemos solo el nombre."""
        return self.name