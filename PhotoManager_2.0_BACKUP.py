import datetime
import sys
import os
from commons.files_operations import *
from commons.folders_ui_utils import select_folder, select_folders_from_parent
from commons.folders_operations import *

try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()

    # Notificació de la inicialització de l'script
    print(f"[{initial_time}] - Initializating process...")

    # Identifiquem la carpeta de Masters
    if len(sys.argv[1:]) > 1 :
        # Si s'ha passat més d'un argument llançarem error, doncs només pot haver-hi una carpeta de masters
        raise Exception("More than one argument not allowed")
    elif len(sys.argv[1:]) == 1:
        # Si només s'ha passat un argument assumim que aquest és la ruta de la carpeta masters
        masters_folder = select_folders_from_parent(sys.argv[1])
    elif sys.argv[1:] != 0:
        # Si no s'ha passat cap argument obrirem un quadre per seleccionar la ruta de la carpeta pare
        masters_folder = select_folder("Select master folder")

    # Identifiquem la carpeta destination com la 
    destination_folder = masters_folder

    # Si existeix la carpeta Edits la seleccionem com a variable
    edits_folder = ""
    if os.path.isdir(os.path.join(masters_folder,"_EDITS")):
        edits_folder = os.path.join(masters_folder,"_EDITS")

################## REVISAR AQUESTA PART
    # Comprovem si la carpeta masters està buida i, si ho està, finalitzem procés
    if is_empty_folder(masters_folder) or is_almost_empty_folder(masters_folder,["@eaDir","thumbs.db", "desktop.ini"]):
        print(f"{masters_folder} is an empty folder")
        sys.exit(1)
    else:
        print(f"The folder {masters_folder} is not an empty folder.\n is_empty_folder={is_empty_folder(masters_folder)}\nis_almost_empty_folder={is_almost_empty_folder(masters_folder,['@eaDir','thumbs.db', 'desktop.ini'])}")
################## REVISAR AQUESTA PART

    # Processem les fotografies obtingudes de l'iphone
    process_photos_from_iphone(masters_folder, edits_folder)

    # Creem una estructura de carpetes basada en les dates i les extensions i traslladem els arxius
    move_files_to_folder_by_date_and_extension(masters_folder)

    # Separem els MOV dels LIVE
    move_live_files_to_diferent_folder(masters_folder)

    # Movem totes les carpetes creades de la carpeta Master a la capeta Destination
    move_content_to_folder(masters_folder, destination_folder)


except Exception as e:
    # General exception handling
    print(f"An error occurred: {e}")

finally:
    # Fem una actualització del status
    print(f"[{datetime.datetime.now()}] Execution complete in {datetime.datetime.now()-initial_time} ms.")

    input("Pres <Enter> to exit ...")