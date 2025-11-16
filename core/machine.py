"""simulador de Maquina de Turing de una cinta"""

from __future__ import annotations 

from typing import Dict, Iterable, List, Optional, Tuple  

from .instant_description import InstantDescription  # Representa cada paso (ID)
from .machine_config import MachineConfig            # Configuracion completa de la MT
from .state import State                             # Clase para modelar estados internamente
from .transition import Transition                   # Transiciones 


class Machine:
    """
    Simulador determinista de Maquina de Turing de una sola cinta.
    """

    def __init__(self, config: MachineConfig, *, max_steps: Optional[int] = None) -> None:
        """
        Construye la maquina a partir de una MachineConfig ya validada

        Parametros:
            config: instancia de MachineConfig construida desde el YAML.
            max_steps: limite para evitar loops infinitos.
        """
        self._config = config

        # Creamos objetos State para cada nombre de estado
        self._states: Dict[str, State] = {name: State(name) for name in config.states}

        # Conjunto de estados de aceptacion 
        self._accept_states = set(config.accept_states)

        # Simbolo blank de la cinta
        self._blank_symbol = config.blank_symbol

        # Limite opcional de pasos
        self._max_steps = max_steps

        # Diccionario (estado, simbolo) -> Transition
        self._transition_map = self._build_transition_map(config.transitions)

    def run(self, input_string: str) -> tuple[list[InstantDescription], bool]:
        """
        Simula la maquina sobre la cadena de entrada dada.

        Retorna:
            - lista de InstantDescription 
            - booleano que indica si la cadena fue aceptada (True) o rechazada (False)
        """
        # Validamos que el input solo use simbolos del alfabeto de entrada
        self._validate_input_string(input_string)

        # Inicializamos la cinta a partir del input
        tape = self._initialize_tape(input_string)

        # El cabezal siempre empieza en la posicion 0
        head_index = 0

        # Estado inicial viene de la configuracion
        current_state = self._config.initial_state

        # Historial de IDs
        history: list[InstantDescription] = [self._snapshot(current_state, tape, head_index)]

        # Caso borde: si el estado inicial ya es de aceptacion, devolvemos de una vez
        if current_state in self._accept_states:
            return history, True

        steps = 0  # Contador de pasos para controlar loops
        while True:
            # Simbolo actual bajo el cabezal
            symbol = tape[head_index]

            # Buscamos la transicion (estado, simbolo) en el diccionario
            transition = self._transition_map.get((current_state, symbol))

            # Si no hay transicion definida, la maquina se detiene y rechaza
            if transition is None:
                return history, False

            # Aplicamos la transicion:
            # 1. Escribimos en la cinta
            tape[head_index] = transition.write_symbol

            # 2. Cambiamos de estado
            current_state = transition.next_state

            # 3. Movemos el cabezal (y expandimos cinta si es necesario)
            head_index = self._move_head(head_index, transition.move, tape)

            # Aumentamos contador de pasos
            steps += 1

            # Guardamos snapshot de la nueva configuracion
            history.append(self._snapshot(current_state, tape, head_index))

            # Si llegamos a un estado de aceptacion, devolvemos aceptado
            if current_state in self._accept_states:
                return history, True

            # Si se alcanzo el maximo de pasos configurado, paramos
            if self._max_steps is not None and steps >= self._max_steps:
                # Aqui devolvemos aceptado solo si ya esta en estado de aceptacion
                return history, current_state in self._accept_states

    def _build_transition_map(
        self, transitions: Iterable[Transition]
    ) -> Dict[Tuple[str, str], Transition]:
        """
        Construye el diccionario (estado, simbolo) -> Transition.

        Ademas valida:
            - No haya transiciones duplicadas para el mismo par (estado, simbolo).
            - Todas las transiciones apunten a estados definidos.
        """
        transition_map: Dict[Tuple[str, str], Transition] = {}
        for transition in transitions:
            key = transition.signature()

            # Una transicion por cada (estado, simbolo) para que sea determinista
            if key in transition_map:
                raise ValueError(
                    "Duplicate transition detected for state/symbol pair "
                    f"{key}. Deterministic machine requires unique transitions."
                )

            # Validamos que el estado de origen exista
            if transition.current_state not in self._states:
                raise ValueError(
                    f"Transition refers to undefined state '{transition.current_state}'."
                )

            # Validamos que el estado destino exista
            if transition.next_state not in self._states:
                raise ValueError(
                    f"Transition jumps to undefined state '{transition.next_state}'."
                )

            transition_map[key] = transition

        return transition_map

    def _validate_input_string(self, input_string: str) -> None:
        """
        Verifica que todos los simbolos del input esten en el alfabeto de entrada.
        """
        tape_symbols = set(self._config.input_alphabet)
        invalid_symbols = [ch for ch in input_string if ch not in tape_symbols]
        if invalid_symbols:
            raise ValueError(
                "Input string contains symbols outside the input alphabet: "
                + ", ".join(sorted(set(invalid_symbols)))
            )

    def _initialize_tape(self, input_string: str) -> List[str]:
        """
        Inicializa la cinta como lista de simbolos.

        Si la cadena esta vacia, se coloca un unico blank.
        """
        if not input_string:
            return [self._blank_symbol]
        return list(input_string)

    def _move_head(self, head_index: int, move: str, tape: List[str]) -> int:
        """
        Mueve el cabezal a la izquierda, derecha o lo deja.

        Si nos salimos de la cinta, la expandimos con simbolos blanks.
        """
        if move == "L":
            # Si estamos al borde izquierdo y nos movemos a la izquierda,
            # insertamos un blank al inicio.
            if head_index == 0:
                tape.insert(0, self._blank_symbol)
                return 0
            return head_index - 1

        if move == "R":
            head_index += 1
            # Si nos movemos una posicion mas alla del final, agregamos un blank.
            if head_index == len(tape):
                tape.append(self._blank_symbol)
            return head_index

        # 'S' (Stay) -> no movemos el cabezal
        return head_index

    def _snapshot(
        self, current_state: str, tape: List[str], head_index: int
    ) -> InstantDescription:
        """
        Construye una InstantDescription a partir del estado interno actual.

        Convierte la cinta a string y guarda la posicion del cabezal.
        """
        tape_str = "".join(tape)
        return InstantDescription(state=current_state, tape=tape_str, head_position=head_index)