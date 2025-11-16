
from __future__ import annotations

from pathlib import Path
from typing import List
import sys

from instant_description import InstantDescription
from machine import Machine
from machine_config import MachineConfig
from parser import Parser


class TuringMachine:
    
    def __init__(self) -> None:
        self.machine: Machine | None = None
        self.config: MachineConfig | None = None

    def load_machine(self, filepath: str | Path) -> None:

        try:
            self.config = Parser.load_from_file(filepath)
            self.machine = Machine(self.config, max_steps=10000)
            
            print(f"Máquina cargada")
            print(f"   Estados: {len(self.config.states)}")
            print(f"   Transiciones: {len(self.config.transitions)}")
            print(f"   Estado inicial: {self.config.initial_state}")
            print(f"   Estados de aceptación: {', '.join(self.config.accept_states)}")
            
        except Exception as e:
            print(f"Error al cargar la máquina: {e}")
            raise

    def run_all_inputs(self) -> None:
        
        if self.machine is None or self.config is None:
            print("Primero debes cargar una máquina.")
            return

        if not self.config.inputs:
            print("No hay inputs definidos en el archivo.")
            return

        for idx, input_string in enumerate(self.config.inputs, 1):
            self.run_single_input(input_string, idx)

    def run_single_input(self, input_string: str, index: int | None = None) -> None:
        
        if self.machine is None:
            print("Primero debes cargar una máquina.")
            return

        header = f"Cadena #{index}" if index else "Cadena"
        print(f"\n{'-'*60}")
        print(f"{header}: \"{input_string}\"")
        print(f"{'-'*60}")

        try:
            history, accepted = self.machine.run(input_string)
            
            print("\nIDs:\n")
            self._display_instant_descriptions(history)
            
            print(f"\n{'─'*60}")
            if accepted:
                print("ACEPTADA")
            else:
                print("RECHAZADA")
            print(f"{'─'*60}")
            
        except Exception as e:
            print(f"Error durante la ejecución: {e}")

    def _display_instant_descriptions(self, history: List[InstantDescription]) -> None:
        
        for idx, id_snapshot in enumerate(history):
            tape_visual = self._format_tape_with_head(
                id_snapshot.tape, 
                id_snapshot.head_position
            )
            
            print(f"{id_snapshot.state:>4s} | {tape_visual}")

    def _format_tape_with_head(self, tape: str, head_position: int) -> str:
       
        if not tape or head_position < 0 or head_position >= len(tape):
            return tape

        before = tape[:head_position]
        symbol = tape[head_position]
        after = tape[head_position + 1:]
        
        return f"{before}[{symbol}]{after}"


def main() -> None:
    
    if len(sys.argv) < 2:
        
        sys.exit(1)

    filepath = sys.argv[1]
    
    cli = TuringMachine()
    
    try:
        cli.load_machine(filepath)
        cli.run_all_inputs()
    except Exception as e:
        print(f"\nError fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()