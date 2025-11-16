import sys
from pathlib import Path

from cli import TuringMachine


def main():
    

    print("SIMULADOR DE MÁQUINA DE TURING")
    
    if len(sys.argv) < 2:
        print("Error: Debes proporcionar un archivo YAML")
        print("\nUso:")
        print("  python main.py <archivo_yaml>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"Error: No se encuentra el archivo '{filepath}'")
        sys.exit(1)
    
    cli = TuringMachine()
    
    try:
        cli.load_machine(filepath)
        cli.run_all_inputs()
        
        print("\n" + "="*60)
        print("Ejecución completada")
        print("="*60 + "\n")
        
   
    except Exception as e:
        print(f"\nError fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()