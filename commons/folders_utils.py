import os
import datetime
from pathlib import Path
import shutil


def files_list(folder_name):
    # Aquesta funció retorna els fitxers continguts en una carpeta en concret
    files = []
    for d in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, d)):
          files.append(os.path.join(folder_name, d))

    return files; 

def subfolders_list (folder_name):
    # Aquesta funció retorna les subcarpetes contingudes en una carpeta en concret
    subfolders = []
    for d in os.listdir(folder_name):
        if os.path.isdir(os.path.join(folder_name, d)):
          subfolders.append(os.path.join(folder_name, d))

    return subfolders

def extract_date(folder_name):
    # Aquesta funció  extreu la data del nom de la carpeta
    return folder_name.split("_")[0]

def extract_date_and_return_date_object(folder_name):
    # Aquesta funció converteix la data del nom de la carpeta a un objecte de data
    data = folder_name.split("_")[0]
    data = data.split(" ")

    return datetime.datetime(int(data[0]),int(data[1]),int(data[2]))

def is_empty_folder(folder_path):
    if os.path.isdir(folder_path):
        return len(os.listdir(folder_path)) == 0
    else:
        print(f"{folder_path} no és una carpeta vàlida.")
        return False

def is_almost_empty_folder(folder_path, last_files):
    if os.path.isdir(folder_path):

        # Obtenim tots els filtxers de la carpeta
        list_of_files = os.listdir(folder_path)

        # Comprovem que tots els fitxers que queden són els esperats en els darrers fitxers de la carpeta
        if all(elem in last_files for elem in list_of_files):
            return True
        else:
            return False

def delete_folder_if_empty(folder, silent_mode=False):
    """
    Elimina una carpeta si està buida o només conté el directori especial `@eaDir`.
    Args:
        carpeta (str): Ruta de la carpeta a comprovar i eliminar.
    Returns:
        bool: True si la carpeta ha estat eliminada, False en cas contrari.
    """

    # Convertim l'string de la ruta en un objecte Path
    folder_path = Path(folder)

    # Comprovar si el directori existeix
    if not folder_path.is_dir():
        print(f"'{folder}' doesn't exist or is not a directory.")
        return False

    # Llistar tots els contents de la carpeta (incloent-hi ocults)
    content = list(folder_path.iterdir())

    # Llista d'elements a ignorar
    ignored_names = {"@eaDir",".DS_Store"}

    # Filtrar per eliminar qualsevol altre element que no sigui cap dels noms ignorats
    filtered_content = [item for item in content if item.name not in ignored_names]

    # Si només queda @eaDir, eliminar-lo
    if len(filtered_content) == 0:
        # Si només hi ha arxius dels tips ignorables o no hi ha res, podem esborrar-lo
        for item in content:
            if item.name in ignored_names:  
                try:
                    if item.is_dir():
                        #os.rmdir(item) Canvi de funció a proposta de Claude (update fet el 9/8/2026) per tal que borri correctament i recursivament @eadir
                        shutil.rmtree(item)
                    else:
						# Per si es un arxiu
                        item.unlink()
                except Exception as e:
                    if not silent_mode:
                        print(f"Not possible to remove '{item}': {e}")
                    return False
        try:
            os.rmdir(folder_path)  # Eliminar la carpeta principal
            return True
        except Exception as e:
            if not silent_mode:
                print(f"Not possible to remove '{folder}': {e}")
            return False
    else:
        if not silent_mode:
            print(f"Not possible to remove '{folder}': folder not empty")
        return False

def move_content_to_folder(container_folder, destination_folder):
    
    # Comprovem si les carpetes existeixen
    if os.path.isdir(container_folder) and os.path.isdir(destination_folder):
        
        # Cerquem de manera recursiva dins totes les carpetes i subcarpetes
        for root, dirs, files in os.walk(container_folder):
            # Excloem carpetes no desitjades
            dirs[:] = [d for d in dirs if d != '@eaDir']

            # Per totes les carpetes contingudes dins del contenidor
            for dir in dirs:
                try:
                    shutil.move(os.path.join(container_folder,dir),destination_folder)
                except Exception as e:
                    print(f"Error trying to move from {os.path.basename(container_folder)} to {os.path.basename(destination_folder)}")

        # Un cop finalitzat el bucle correctament finalitzem retornant True
        return True

    else:
        return False