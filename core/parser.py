
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from machine_config import MachineConfig
from transition import Transition


class Parser:
    
    @staticmethod
    def load_from_file(filepath: str | Path) -> MachineConfig:
        
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValueError("El archivo YAML debe contener un diccionario.")

        if "mt" not in data:
            raise ValueError("El archivo YAML debe contener una clave 'mt'.")

        mt_data = data["mt"]
        return Parser._parse_machine_config(mt_data, data.get("inputs"))

    @staticmethod
    def _parse_machine_config(mt_data: Dict[str, Any], inputs: List[str] | None) -> MachineConfig:
        """
        Convierte el diccionario de la sección 'mt' en un MachineConfig.
        """
        required_keys = {
            "states",
            "input_alphabet",
            "tape_alphabet",
            "initial_state",
            "accept_states",
            "transitions",
        }
        missing_keys = required_keys - set(mt_data.keys())
        if missing_keys:
            raise ValueError(f"Faltan claves requeridas en 'mt': {missing_keys}")

        transitions = Parser._parse_transitions(mt_data["transitions"])

        blank_symbol = mt_data.get("blank_symbol", "B")

        return MachineConfig(
            states=mt_data["states"],
            input_alphabet=mt_data["input_alphabet"],
            tape_alphabet=mt_data["tape_alphabet"],
            initial_state=mt_data["initial_state"],
            accept_states=mt_data["accept_states"],
            transitions=transitions,
            inputs=inputs,
            blank_symbol=blank_symbol,
        )

    @staticmethod
    def _parse_transitions(transitions_data: List[Dict[str, Any]]) -> List[Transition]:
        
        if not isinstance(transitions_data, list):
            raise ValueError("'transitions' debe ser una lista.")

        transitions: List[Transition] = []

        for idx, trans_dict in enumerate(transitions_data):
            if not isinstance(trans_dict, dict):
                raise ValueError(f"La transición #{idx} debe ser un diccionario.")

            required = {"state", "read", "write", "move", "next"}
            if not required.issubset(trans_dict.keys()):
                missing = required - set(trans_dict.keys())
                raise ValueError(f"La transición #{idx} no tiene las claves: {missing}")

            current_state = trans_dict["state"]
            next_state = trans_dict["next"]
            move = trans_dict["move"]

            read_symbols = Parser._normalize_symbol_field(trans_dict["read"], "read")
            write_symbols = Parser._normalize_symbol_field(trans_dict["write"], "write")

            if len(read_symbols) != len(write_symbols):
                raise ValueError(
                    f"La transición #{idx} tiene diferente cantidad de símbolos "
                    f"en 'read' ({len(read_symbols)}) y 'write' ({len(write_symbols)})."
                )

            for read_sym, write_sym in zip(read_symbols, write_symbols):
                transitions.append(
                    Transition(
                        current_state=current_state,
                        read_symbol=read_sym,
                        write_symbol=write_sym,
                        move=move,
                        next_state=next_state,
                    )
                )

        return transitions

    @staticmethod
    def _normalize_symbol_field(value: Any, field_name: str) -> List[str]:
       
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            if not all(isinstance(s, str) for s in value):
                raise ValueError(f"Todos los elementos de '{field_name}' deben ser strings.")
            return value
        raise ValueError(f"'{field_name}' debe ser un string o una lista de strings.")