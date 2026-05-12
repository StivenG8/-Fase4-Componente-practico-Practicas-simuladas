import sys
import os
import logging
import tkinter as tk

# Aseguramos que Python encuentre las carpetas locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main.frontend.app_interfaz import InterfazSistema

def main():
    # Configuramos el logging para todo el sistema
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'errores_sistema.log')
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("=== INICIO DE LA APLICACIÓN ===")
    
    root = tk.Tk()
    app = InterfazSistema(root)
    root.mainloop()

if __name__ == "__main__":
    main()
