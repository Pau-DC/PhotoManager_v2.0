import datetime
import sys
import os
import subprocess
import traceback
from commons.tee_stream import Tee
from commons.files_operations import *
from commons.folders_operations import *
from commons.folders_ui_utils import select_folder


def notify(title, message):
    # Mostra una notificació de macOS (útil quan s'executa des d'Automator, on no es veu la sortida)
    try:
        message = message.replace('"', "'")
        subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}"'], check=False)
    except Exception:
        pass


# Inicialització de la variable de temps
initial_time = datetime.datetime.now()

# Inicialització del fitxer de log (un fitxer per execució) a ~/Library/Logs/PhotoManager
log_dir = os.path.expanduser("~/Library/Logs/PhotoManager")
os.makedirs(log_dir, exist_ok=True)
log_filepath = os.path.join(log_dir, f"{initial_time.strftime('%Y%m%d%H%M%S')}_MoveRelated.log")
log_file = open(log_filepath, "w", encoding="utf-8")

# Redirigim stdout i stderr a la consola i al fitxer de log alhora
original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = Tee(original_stdout, log_file)
sys.stderr = Tee(original_stderr, log_file)

files_not_moved = []

try:
    # Notificació de la inicialització de l'script
    print(f"[{initial_time}] - Initializating process...")
    print(f"Arguments rebuts: {sys.argv[1:]}")

    # Comprovem si s'ha obtingut el fitxer com a argument
    if len(sys.argv) < 2:
        raise Exception("No file selected")

    # Seleccionem el nou directori on volem moure els arxius
    new_folder = select_folder("Select new folder")
    if not new_folder:
        raise Exception("No s'ha seleccionat cap carpeta de destí (cancel·lat)")
    print(f"Carpeta de destí: {new_folder}")

    # Per cada fitxer seleccionat
    for file in sys.argv[1:]:
        jpg_file = os.path.abspath(file)
        print(f"\n--- {jpg_file}")

        try:
            # Busquem els fitxers relacionats i els registrem al log
            related_files = find_related_files(jpg_file)
            for key, subdict in related_files.items():
                print(f"\t{key}: {subdict['SOURCE_ABS_PATH']}")

            # Movem els fitxers
            move_files_to_related_folder(related_files, new_folder)

            # Comprovem que realment s'han mogut tots (si l'origen encara existeix, no s'ha mogut)
            for key, subdict in related_files.items():
                if os.path.exists(subdict['SOURCE_ABS_PATH']):
                    print(f"\tNO MOGUT ({key}): {subdict['SOURCE_ABS_PATH']}")
                    files_not_moved.append(subdict['SOURCE_ABS_PATH'])

        except Exception as e:
            # Un error en un fitxer no atura la resta
            print(f"\tERROR amb {jpg_file}: {e}")
            traceback.print_exc()
            files_not_moved.append(jpg_file)

except Exception as e:
    # General exception handling
    print(f"An error occurred: {e}")
    traceback.print_exc()
    files_not_moved.append("(error general)")

finally:
    # Fem una actualització del status
    print(f"\n[{datetime.datetime.now()}] Execution complete in {datetime.datetime.now()-initial_time} ms.")

    # Avisem amb una notificació del resultat
    if files_not_moved:
        print(f"Fitxers no moguts: {len(files_not_moved)}")
        notify("MoveRelated ⚠️", f"{len(files_not_moved)} fitxer(s) no s'han mogut. Mira el log a ~/Library/Logs/PhotoManager")
    else:
        notify("MoveRelated ✅", "Tots els fitxers s'han mogut correctament")

    # Restaurem la sortida estàndard i tanquem el fitxer de log
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    log_file.close()