import datetime
import sys
import os
from commons.files_operations import *
from commons.folders_operations import *
from commons.folders_ui_utils import select_folder

try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()

    # Notificació de la inicialització de l'script
    print(f"[{initial_time}] - Initializating process...")

    # Comprovem si s'ha obtingut el fitxer com a argument

    if len(sys.argv) < 2:
        raise Exception("No file selected")
        sys.exit(1)

    # Seleccionem el nou directori on volem moure els arxius
    new_folder = select_folder("Select new folder")

    
    # Obtenim el fitxer seleccionat
    for file in sys.argv[1:]:
        jpg_file = file

        # Movem totes les carpetes creades de la carpeta Master a la capeta Destination
        related_files = find_related_files(jpg_file)
        move_files_to_related_folder(related_files, new_folder)


except Exception as e:
    # General exception handling
    print(f"An error occurred: {e}")

finally:
    # Fem una actualització del status
    print(f"[{datetime.datetime.now()}] Execution complete in {datetime.datetime.now()-initial_time} ms.")

    # Tanquem el fitxer de log en acabar l'execució
    sys.stdout.close()
