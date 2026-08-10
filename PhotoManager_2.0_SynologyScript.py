import datetime
import sys
import os
from commons.tee_stream import Tee
from commons.files_operations import *
from commons.folders_operations import *


try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()

    # Inicialització del fitxer d'output i creació de la carpeta d'outputs si no existeix
    log_filename = f"{initial_time.strftime('%Y%m%d%H%M%S')}_output.log"
    output_dir = "/volume1/Scripts_outputs/Photos_Manager_Scripts_outputs"
    os.makedirs(output_dir, exist_ok=True)
    log_filepath = os.path.join(output_dir, log_filename)

    # Redirigeix la sortida estàndard (stdout) al fitxer de logs
#    sys.stdout = open(log_filepath, 'w')
    log_file = open(log_filepath, 'w')
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = Tee(original_stdout, log_file)
    sys.stderr = Tee(original_stderr, log_file)

    # Notificació de la inicialització de l'script
    print(f"[{initial_time}] - Initializating process...")

    # Identifiquem les carpeta de Masters i Destination
    masters_folder = "/volume1/homes/NAS_PA_ADMIN/Photos_Manager/1_To_Process/"
    destination_folder = "/volume1/homes/NAS_PA_ADMIN/Photos_Manager/3_To_Move/"

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

    # Tanquem el fitxer de log en acabar l'execució
#    sys.stdout.close()
    log_file.close()
