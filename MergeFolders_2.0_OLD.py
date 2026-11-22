import datetime
import sys
from commons.folders_operations import merge_folders
from commons.folders_ui_utils import select_folders_from_parent

try:
    # Inicialització de la variable de 
    temps_inicial = datetime.datetime.now()

    # Identifiquem les carpetes que volem fusionar
    ### (!) A MILLORAR: Caldria comprovar que els arguments passats per argv són realment paths o carpetes
    if len(sys.argv[1:]) > 1 :
        # Si s'ha passat més d'un argument assumim que són les diferents carpetes que volem fusionar
        selected_folders = sys.argv[1:]
    elif len(sys.argv[1:]) == 1:
        # Si només s'ha passat un argument assumim que aquest és la ruta de la carpeta pare
        selected_folders = select_folders_from_parent(sys.argv[1])
    elif sys.argv[1:] != 0:
        # Si no s'ha passat cap argument obrirem un quadre per seleccionar la ruta de la carpeta pare
        selected_folders = select_folders_from_parent()

    # Activem la funció "merge" de les carpetes
    merge_folders(selected_folders)

except Exception as e:
    # General exception handling
    print(f"An error occurred: {e}")

finally:
    print(f"Execution complete in {datetime.datetime.now()-temps_inicial} ms.")
    input("Pres <Enter> to exit ...")