import os
import datetime
import shutil
import tkinter as tk
from tkinter import filedialog

def select_folders_from_parent(parent=""):
  root = tk.Tk()
  root.withdraw()  # Oculta la finestra principal
  if parent == "":
    parent = filedialog.askdirectory(
    title="Selecciona la carpeta principal que conté les carpetes a fusionar" 
  )
  return subfolders_list(parent)


def files_list(folder_name):
    # Aquesta funció retorna els fitxers continguts en una carpeta en concret
    files = []
    for d in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, d)):
          files.append(os.path.join(folder_name, d))

    return files; 


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

def subfolders_list (folder_name):
    # Aquesta funció retorna les subcarpetes contingudes en una carpeta en concret
    subfolders = []
    for d in os.listdir(folder_name):
        if os.path.isdir(os.path.join(folder_name, d)):
          subfolders.append(os.path.join(folder_name, d))

    return subfolders

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
