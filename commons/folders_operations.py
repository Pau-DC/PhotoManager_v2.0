import os
import shutil
from commons.folders_utils import *
from commons.files_utils import get_creation_date

def copy_files_recursively(origin_folder, destination_folder, relative_root_path=""):

  try:
    # Preparem les variables dels arxius que contenen la carpeta actual
    files = files_list(origin_folder)
    subfolders = subfolders_list(origin_folder)
    relative_path = ""
    num_files = 0

    if origin_folder.startswith(relative_root_path):
      relative_path = origin_folder[len(relative_root_path)+1:]

    # Per tots els arxius dins de la carpeta origen carreguem les variables i movem els arxius a carpeta destí
    for file in files:

      origin_path = file
      file_basename = os.path.basename(file)
      destination_path = os.path.join(destination_folder,relative_path,file_basename)

      # Creem els directoris si no existeixen
      if not os.path.exists(os.path.join(destination_folder,relative_path)):
        os.makedirs(os.path.join(destination_folder,relative_path))

      if os.path.isfile(origin_path):
        shutil.move(origin_path,destination_path)
        num_files += 1

    # Per totes les subcarpetes dins de la carpeta origen carreguem les variables i movem els arxius a carpeta destí
    for subfolder in subfolders:

      subfolder_basename = os.path.basename(subfolder)

      # Comprobem si es tracta d'una carpeta buida que no existeix en destí i si és el cas la movem
      if is_empty_folder(subfolder) and not os.path.exists(os.path.join(destination_folder,subfolder_basename)):
        os.makedirs(os.path.join(destination_folder,subfolder_basename))

      # Per cada carpeta realitzarem el mateix procés (recursivament)
      num_files = num_files+copy_files_recursively(subfolder,destination_folder,relative_root_path)

      # Comprobem si hem buidat correctament la carpeta i si ho està, la borrem
      if is_empty_folder(subfolder):
        os.rmdir(subfolder)

    return num_files

  except Exception as e:
    # General exception handling
    print(f"ERROR! S'ha produït un error en el procés de copia recursiva de fitxer. Error: {e}")

def merge_folders (folders):

  try:
    # Inicialitzem les variables necessàries
    first_date = ""
    first_date_folder = ""
    num_files_moved = 0

    # Per totes les folders seleccionades
    for actual_folder in folders:

      # Carreguem les variables necessàries
      folder_name = os.path.basename(actual_folder)
      subfolders = subfolders_list(actual_folder)

      # Assignem la data més antiga a la primera carpeta (actual)
      if first_date == "":
        first_date = extract_date(folder_name)
        first_date_folder = actual_folder

      # Comprovem si la carpeta actual és més nova que la guardada com antiga i si ho és actualitzem valors 
      if extract_date_and_return_date_object(first_date) > extract_date_and_return_date_object(folder_name):
        first_date = extract_date(folder_name)
        first_date_folder = actual_folder

      # Movem els arxius de la carpeta actual a la més antiga (si aplica)
      if first_date_folder != actual_folder:
        num_files_moved += copy_files_recursively(actual_folder, first_date_folder, actual_folder)

      # Eliminem la carpeta actual un cop sigui buida
      if is_empty_folder(actual_folder):
        os.rmdir(actual_folder)

    # Informem del nombre d'arxius moguts i carpetes eliminades
    print(f"Informe:\n\tArxius moguts: {num_files_moved}")


  except Exception as e:
    # General exception handling
    print(f"ERROR! S'ha produït un error en el procés de fusió de carpetes. Error: {e}")

def move_files_to_folder_by_date_and_extension(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Creating folders by files date...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        files = files_list(masters_folder)
        num_folders_created = 0 
        num_moved_files = 0 

        # Per tots els arxius
        for file in files:
      			# Carreguem les variables necessàries per moure l'arxiu
            file_basename = os.path.basename(file)
            file_extension = os.path.splitext(file_basename)[1].lstrip(".")
            file_basename_without_extension = os.path.splitext(file_basename)[0]
            creation_date = get_creation_date(file)
            destination_path = ""

            # Comprovem si existeix la carpeta i si no existeix la creem
            date_folder = f"{creation_date} _"
            date_folder_path = os.path.join(masters_folder,date_folder)
            if not os.path.isdir(date_folder_path):
              os.makedirs(date_folder_path, exist_ok=True)
              num_folders_created += 1
            destination_path = date_folder_path

            # Si l'extensió és diferent de JPG movem l'arxiu dins la carpeta de l'extensió, que crearem si no existeix
            if file_extension.upper() != "JPG":
              if file_extension.upper() != "JPEG":
                extension_folder = f"_{file_extension.upper()}"
                extension_folder_path = os.path.join(date_folder_path,extension_folder)
                if not os.path.isdir(extension_folder_path):
                  os.makedirs(extension_folder_path, exist_ok=True)
                destination_path = extension_folder_path

            # Movem el fitxer actual a la carpeta destinació
            shutil.move(file,destination_path)
            num_moved_files += 1

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_folders_created} folders created")
        print(f"\t |-- {num_moved_files} files moved")

def move_live_files_to_diferent_folder(masters_folder):
  try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Moving live file...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        num_moved_files = 0 

        # Cerquem de manera recursiva dins totes les carpetes i subcarpetes
        for root, dirs, files in os.walk(masters_folder):

          # Per tots els fitxers
          for file in files:
            if file.endswith("_LIVE.MOV"):
              destination_path = os.path.join(root,"_LIVE")
              os.makedirs(destination_path, exist_ok=True)
              shutil.move(os.path.join(root,file),destination_path)
              num_moved_files += 1            

  except Exception as e:
      # General exception handling
      print(f"An error occurred: {e}")

  finally:
      print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
      print(f"\t |-- {num_moved_files} files moved")

def move_files_to_related_folder(related_files, new_folder):
  try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()
    print(f"\t + [{initial_time}] Moving related files of {related_files['JPG']['BASENAME']} to new folder...")

    # Preparem les variables dels arxius que contenen la carpeta actual
    num_moved_files = 0
    source_path = ""
    destination_path = ""
    new_folder = os.path.normpath(new_folder)

    # Iterem el diccionari per moure fitxer a fitxer
    for key,subdict in related_files.items():
      source_path = subdict['SOURCE_ABS_PATH']
      destination_path = os.path.join(new_folder,subdict['RELATIVE_PATH'])
      os.makedirs(destination_path, exist_ok=True)
      shutil.move(source_path,destination_path)
      num_moved_files += 1

  except Exception as e:
    # General exception handling
    print(f"An error occurred: {e}")

  finally:
      print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
      print(f"\t |-- {num_moved_files} files moved to related folder")

def move_files_to_relative_path(files, origin_root_path, subfolder):
  try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()
    print(f"\t + [{initial_time}] Moving files to subfolder /{subfolder}")

    # Preparem les variables dels arxius que contenen la carpeta actual
    num_moved_files = 0
  
    #Iterem entre tots els fitxers
    for f in files:
      relative_path = f.relative_to(origin_root_path).parent
      source_path = os.path.join(origin_root_path,relative_path,os.path.basename(f))
      destination_path = os.path.join(origin_root_path,subfolder,relative_path)
      os.makedirs(destination_path, exist_ok=True)
      shutil.move(source_path,destination_path)
      num_moved_files += 1


  finally:
      print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
      print(f"\t |-- {num_moved_files} files moved to folder /{subfolder}")

       
def delete_empty_folders(root_folder):
    
  try:
    # Inicialització de la variable de temps
    initial_time = datetime.datetime.now()
    print(f"\t + [{initial_time}] Deleting empty folders from {root_folder}")

    # Preparem les variables dels arxius que contenen la carpeta actual
    deleted_folders = 0

    # Obtenim el path de la carpeta root
    root_path = Path(root_folder)
    
    # Per cada carpeta, comprovem si està buida i si ho està l'eliminem
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
      if delete_folder_if_empty(Path(dirpath),True):
          deleted_folders += 1

  finally:
      print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
      print(f"\t |-- {deleted_folders} folders removed")

    