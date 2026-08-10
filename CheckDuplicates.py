import datetime
import sys
import argparse
from commons.compare_folders import *
from commons.folders_operations import *
from commons.arguments_utils import *
from commons.folders_ui_utils import select_folder

try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()

    # Identifiquem els arguments que ens arriben i els parsegem 
    ap = argparse.ArgumentParser(description="Check if files are duplicated from an origen to a target folder")
    ap.add_argument("--original", type=Path)
    ap.add_argument("--target", type=Path)
    args = ap.parse_args()

    # Assignem els valors parsejats a les variable corresponents i 
    original_folder = check_args_if_folder_and_return_path(args.original,"Select original folder")
    target_folder = check_args_if_folder_and_return_path(args.target,"Select target folder")

    print(f"original_folder: {original_folder}")
    print(f"target_folder: {target_folder}")

    # Creem un índex ràpid a partir de la mida i un fast hash de tots els arxius 
    fast_index = indexing_target_folder (target_folder)

    # Cridem la funció de comparació de les carpetes a partir de les imatges originals i l'índex que hem creat
    duplicates_collection, news_collection = compare_folders(original_folder, fast_index)

    # Guardem els fitxers organitzats segons si són  arxius duplicats o nous, mantenint el seu path relatiu
    move_files_to_relative_path(duplicates_collection, original_folder, "1_DuplicatedFiles")
    move_files_to_relative_path(news_collection, original_folder, "2_NewFiles")

    #Eliminem les carpetes que estiguin buides
    delete_empty_folders(original_folder)

except Exception as e:
    # General exception handling
    print(f"An error occurred: {e}")

finally:
    print(f"Execution complete in {datetime.datetime.now()-initial_time} ms.")
    input("Pres <Enter> to exit ...")