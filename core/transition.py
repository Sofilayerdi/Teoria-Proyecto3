"""Definicion de una transicion usada por el backend de la Maquina de Turing."""

from __future__ import annotations 

from dataclasses import dataclass  

# movimientos validos: Left, Right, o Stay
_VALID_MOVES = {"L", "R", "S"}


@dataclass(slots=True)
class Transition:
    """
    Representa una regla de transicion determinista de la maquina.

    Teniendo (current_state, read_symbol) se decide:
        - que escribir en la cinta (write_symbol)
        - hacia donde moverse (move)
        - a que estado saltar (next_state)
    """

    current_state: str   # Estado actual 
    read_symbol: str     # Simbolo que debe leerse en la cinta para aplicar esta transicion
    write_symbol: str    # Simbolo que se escribe en la cinta al aplicar la transicion
    move: str            # Movimiento del cabezal: "L", "R" o "S"
    next_state: str      # Estado al que se pasa despues de aplicar la transicion

    def __post_init__(self) -> None: 
        """Validaciones basicas al crear la transicion."""
        # Validamos que el movimiento sea uno de los permitidos
        if self.move not in _VALID_MOVES:
            raise ValueError(
                f"Invalid move '{self.move}'. Expected one of {sorted(_VALID_MOVES)}."
            )

        # Validamos que todos los campos de texto sean strings no vacios
        for attr_name in ("current_state", "read_symbol", "write_symbol", "next_state"):
            value = getattr(self, attr_name)
            if not isinstance(value, str) or value == "":
                raise ValueError(f"{attr_name} must be a non-empty string.")

    def signature(self) -> tuple[str, str]:
        """
        Devuelve la llave que usa la maquina para buscar esta transicion.

        La maquina guarda un diccionario y se retorna la tupla:
            (current_state, read_symbol) -> Transition
        """
        return (self.current_state, self.read_symbol)