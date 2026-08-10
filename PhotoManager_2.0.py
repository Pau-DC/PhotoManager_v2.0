import datetime
import sys
import os
import argparse
from commons.tee_stream import Tee
from commons.files_operations import *
from commons.arguments_utils import *
from commons.folders_operations import *

try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()

    # Identifiquem els arguments que ens arriben i els parsegem 
    ap = argparse.ArgumentParser(description="Organize iPhone photos in chronological folders and extension subfolders")
    ap.add_argument("--masters", type=Path)
    ap.add_argument("--destination", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    # Assignem els valors parsejats a les variable corresponents i 
    masters_folder = check_args_if_folder_and_return_path(args.masters,"Select masters folder")
    destination_folder = check_args_if_folder_and_return_path(args.destination,"Select destination folder")
    output_folder = check_args_if_folder_and_return_path(args.output,"Select output folder")


    # Inicialització del fitxer d'output i creació de la carpeta d'outputs si no existeix
    log_filename = f"{initial_time.strftime('%Y%m%d%H%M%S')}_output.log"
    os.makedirs(output_folder, exist_ok=True)
    log_filepath = os.path.join(output_folder, log_filename)

    # Redirigeix la sortida estàndard (stdout) al fitxer de logs
#    sys.stdout = open(log_filepath, 'w')
    log_file = open(log_filepath, 'w')
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = Tee(original_stdout, log_file)
    sys.stderr = Tee(original_stderr, log_file)

    # Si existeix la carpeta Edits la seleccionem com a variable
    edits_folder = ""
    if os.path.isdir(os.path.join(masters_folder,"_EDITS")):
        edits_folder = os.path.join(masters_folder,"_EDITS")

    # Notificació de la inicialització de l'script
    print(f"[{initial_time}] - Initializating process...")

################## REVISAR AQUESTA PART
    # Comprovem si la carpeta masters està buida i, si ho està, finalitzem procés
    if is_empty_folder(masters_folder) or is_almost_empty_folder(masters_folder,["@eaDir","thumbs.db", "desktop.ini"]):
        print(f"{masters_folder} is an empty folder")
        sys.exit(1)
    else:
        print(f"The folder {masters_folder} is not an empty folder.\n--> is_empty_folder={is_empty_folder(masters_folder)}\n--> is_almost_empty_folder={is_almost_empty_folder(masters_folder,['@eaDir','thumbs.db', 'desktop.ini'])}")
################## REVISAR FINS AQUÍ 

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