"""Descripcion instantanea (Instant Description) de una configuracion de la Maquina de Turing."""

from __future__ import annotations  

from dataclasses import dataclass  


@dataclass(slots=True)
class InstantDescription:
    """
    Estructura de solo lectura que describe una configuracion de la maquina.

    Contiene:
        - state: estado actual (nombre)
        - tape: contenido completo de la cinta como cadena
        - head_position: indice donde esta parado el cabezal
    """

    state: str          # Estado actual (como string)
    tape: str           # Representacion de la cinta en paso actual
    head_position: int  # Posicion (indice) del cabezal sobre la cinta

    def __post_init__(self) -> None:  
        """Validaciones basicas ."""
        if not isinstance(self.state, str) or self.state == "":
            raise ValueError("state must be a non-empty string.")
        if not isinstance(self.tape, str):
            raise ValueError("tape must be a string representation.")
        if not isinstance(self.head_position, int) or self.head_position < 0:
            raise ValueError("head_position must be a non-negative integer index.")