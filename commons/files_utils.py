import datetime
import subprocess
import re
import pillow_heif
from commons.folders_utils import *
from commons.common_utils import *
from PIL import Image

def uppercase_files_extension(masters_folder):

    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Updating all extensions to uppercase...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        files = files_list(masters_folder)
        num_uppercase_extension_updtaded_files = 0 
        
        # Per tots els arxius
        for file in files:

            # Definim les variables d'arxiu necessàries
            file_basename = os.path.basename(file)
            file_basename_without_extension = os.path.splitext(file_basename)[0]
            file_extension = os.path.splitext(file_basename)[1]
            if file_extension.islower():
                file_old_path = os.path.join(masters_folder, file_basename_without_extension+file_extension)
                file_new_path = os.path.join(masters_folder, file_basename_without_extension+file_extension.upper())
                os.rename(file_old_path,file_new_path)
                num_uppercase_extension_updtaded_files += 1

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_uppercase_extension_updtaded_files} extensions updated to uppercase")
        

def identify_lives(masters_folder):

    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying lives...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        files = files_list(masters_folder)
        num_live_files = 0 

        # Per tots els arxius
        for file in files:

            # Definim les variables d'arxiu necessàries
            file_basename = os.path.basename(file)
            file_basename_without_extension = os.path.splitext(file_basename)[0]



            # Comprovem que sigui tipus .mov i que exiteix un arxiu amb el mateix nom de tipus heic
            if file.lower().endswith(".mov"):
                if os.path.isfile(os.path.join(masters_folder,file_basename_without_extension+".HEIC")):

                    ### (!) A MILLORAR: En l'script antic de Apple Script comprovaba que el media group i content identifier coincidien
                    # -- Extraiem el GroupID del HEIC el CONTENT ID del MOV i comprovem que realment el comparteixin
                    # set contentID to (do shell script "/usr/local/bin/exiftool -s3 -ContentIdentifier " & pathArxiuMovPOSIX)
                    # set mediaGroupID to (do shell script "/usr/local/bin/exiftool -s3 -MediaGroupUUID " & pathArxiuHeicPOSIX)      

                    # if contentID is mediaGroupID then
                    # Renombrem el nom del fitxer afegint el sufix "_LIVE"
                    os.rename(file,os.path.join(masters_folder,file_basename_without_extension+"_LIVE.MOV"))
                    num_live_files += 1

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_live_files} files identifyied as lives")

def identify_modifs_in_edits_folder(masters_folder, edits_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying modified files...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        modif_files = files_list(edits_folder)
        num_modif_files = 0 

        # Per tots els arxius
        for modif_file in modif_files:

            # Definim les variables d'arxiu necessàries
            modif_file_basename = os.path.basename(modif_file)
            modif_file_basename_without_extension = os.path.splitext(modif_file_basename)[0]
            modif_file_extension = os.path.splitext(modif_file_basename)[1]
            modif_parent_folder = os.path.dirname(os.path.dirname(modif_file))

            # Renombrem el nom del fitxer afegint el sufix "_MODIF" i el movem a la carpeta superior
            os.rename(modif_file,os.path.join(modif_parent_folder,modif_file_basename_without_extension+"_MODIF"+modif_file_extension))
            num_modif_files += 1

        # Si la carpeta EDITS està buida l'eliminem. Primer ens hem d'assegurar de borrar el fitxer @eaDir que crea Synology
        delete_folder_if_empty(edits_folder)

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_modif_files} files identifyied as modified files")

def identify_modifs(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying modified files...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        modif_files = files_list(masters_folder)
        num_modif_files = 0 

        # Per tots els arxius
        for modif_file in modif_files:

            # Definim les variables d'arxiu necessàries
            modif_file_basename = os.path.basename(modif_file)
            modif_file_basename_without_extension = os.path.splitext(modif_file_basename)[0]
            modif_file_extension = os.path.splitext(modif_file_basename)[1]
            modif_parent_folder = os.path.dirname(os.path.dirname(modif_file))

            if modif_file_basename.upper().startswith("IMG_E"):
                # Renombrem el nom del fitxer afegint el sufix "_MODIF" i el movem a la carpeta superior
                modif_file_basename_without_extension_renamed = modif_file_basename_without_extension.replace("IMG_E","IMG_")
                os.rename(modif_file,os.path.join(os.path.dirname(modif_file),modif_file_basename_without_extension_renamed+"_MODIF"+modif_file_extension))
                num_modif_files += 1

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_modif_files} files identifyied as modified files")

def convert_HEIC_to_JPG(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Converting HEIC files to JPG...")

         # Preparem les variables dels arxius que contenen la carpeta actual
        files = files_list(masters_folder)
        num_converted_files = 0
        num_failed_files = 0


        # Per tots els arxius
        for file in files:

            # Preparem les variables necessàries
            file_basename = os.path.basename(file)
            file_basename_without_extension = os.path.splitext(file_basename)[0]

            # Per cada fitxer tipus HEIC el convertim a JPG
            if file.lower().endswith(".heic"):
                    try:
                        heif_file = pillow_heif.open_heif(file)
                        image = Image.frombytes(
                            heif_file.mode, 
                            heif_file.size, 
                            heif_file.data,
                        )
                        image.save(os.path.join(masters_folder,file_basename_without_extension+".JPG"), "JPEG")

                        # Per cada fitxer creat preparem la comanda fent ús d'ExifTool i en tractem el resultat
                        comand = ["exiftool","-tagsFromFile",f"{os.path.join(masters_folder,file_basename_without_extension)}.HEIC","-all:all","-FileModifyDate","-Orientation=1","-n","-overwrite_original",f"{os.path.join(masters_folder,file_basename_without_extension)}.JPG"]
                        result = execute_comand(comand)
                        num_converted_files += extract_int_from_output(result, "image files updated")

                    except Exception as file_error:
                        # Error específic d'aquest fitxer: el registrem i seguim amb la resta
                        num_failed_files += 1
                        print(f"\t |-- ERROR converting {file_basename}: {file_error}")
                        continue

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_converted_files} updated files")
        print(f"\t |-- {num_failed_files} files failed to convert")

def identify_slowmotion(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying slowmotion...")

        # Preparem les variables globals de la funció
        framerate_limit = 60
        num_slowmotion_files = 0 

        # Preparem el llistat d'arxius tipus MOV i que contenen el tag un framerate superior al límit definit
        comand = [
            "exiftool",  # eina de línia de comandes per gestionar metadades
            "-s3",  # retornar només el valor de les etiquetes
            "-n",  # mostrar els valors numèrics de les etiquetes sense formatejar
            "-if",  # afegir condició de filtre
            f"$FileType eq 'MOV' and $VideoFrameRate > {framerate_limit}",  # condició
            "-p",  # definir el format de sortida
            "$FilePath",  # mostrar les rutes completes dels fitxers
            "-m",  # ignorar advertències
            "-q",  # mode silenciós
            "-q",  # mode silenciós doble
            f"{masters_folder}" #directori a explorar
        ]
        result = execute_comand(comand)

        #Si la comanda obté resposta processem el resultat de la comanda
        if(result!=""):
            files = result.splitlines()

            # Per cada fitxer
            for file in files:
                # Preparem les variables necessàries
                file_basename = os.path.basename(file)
                file_basename_without_extension = os.path.splitext(file_basename)[0]

                # Renombrem el nom del fitxer afegint el sufix "_SLOWMOTION"
                os.rename(file,os.path.join(masters_folder,file_basename_without_extension+"_SLOWMOTION.MOV"))
                num_slowmotion_files += 1

            
    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_slowmotion_files} files identifyied as slowmotion")

def identify_timelapse(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying timelapse...")

        # Preparem les variables globals de la funció
        num_timelapse_files = 0 

        # Preparem el llistat d'arxius tipus MOV i que contenen el tag que identifica els timelapses
        comand = [
            "exiftool",  # eina de línia de comandes per gestionar metadades
            "-s3",  # retornar només el valor de les etiquetes
            "-n",  # mostrar els valors numèrics de les etiquetes sense formatejar
            "-if",  # afegir condició de filtre
            f"$FileType eq 'MOV' and $capturemode eq 'Time-lapse'", # condició
            "-p",  # definir el format de sortida
            "$FilePath",  # mostrar les rutes completes dels fitxers
            "-m",  # ignorar advertències
            "-q",  # mode silenciós
            "-q",  # mode silenciós doble
            f"{masters_folder}" #directori a explorar
        ]
        result = execute_comand(comand)

        #Si la comanda obté resposta processem el resultat de la comanda
        if(result!=""):
            files = result.splitlines()

            # Per cada fitxer
            for file in files:
                # Preparem les variables necessàries
                file_basename = os.path.basename(file)
                file_basename_without_extension = os.path.splitext(file_basename)[0]

                # Renombrem el nom del fitxer afegint el sufix "_TIMELAPSE"
                os.rename(file,os.path.join(masters_folder,file_basename_without_extension+"_TIMELAPSE.MOV"))
            num_timelapse_files += 1

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_timelapse_files} files identifyied as timelapse")

def update_files_dates_from_folder(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Updating dates...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        num_updated_files = 0 

        # Preparem la comanda fent ús d'ExifTool i en tractem el resultat
        comand = ["exiftool","-overwrite_original","-m","-AllDates<createDate","-FileModifyDate<createDate","-ext", "jpg", "-ext", "heic","-AllDates<creationDate","-FileModifyDate<creationDate","-ext","mov","-AllDates<DateTimeOriginal","-FileModifyDate<DateTimeOriginal","-ext","png",f"{masters_folder}"]
        result = execute_comand(comand)
        num_updated_files += extract_int_from_output(result, "image files updated")

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_updated_files} updated files")

def update_file_dates_from_file(file):
    try:
        # Revisem el tipus d'extensió per capturar una metadata o una altre
        original_date = "createDate"
        if file.lower().endswith(".mov"):
            original_date = "creationDate"
        elif file.lower().endswith(".png"):
            original_date = "DateTimeOriginal"


        # Per cada arxiu apliquem la comanda fent ús de ExifTool i en tractem el resultat
        comand = ["exiftool","-overwrite_original",f"-AllDates<{original_date}",f"-FileModifyDate<{original_date}",f"{file}"]
        result = execute_comand(comand)
        num_updated_files += extract_int_from_output(result, "image files updated")

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")
        return 0

def get_creation_date(file):
    try:
        # Obtenim la data de creació mitjançant Exiftool
        comand = ["exiftool","-s3",f"-createDate",f"{file}"]
        create_date = execute_comand(comand)
        create_date_without_hour = "".join(create_date.split(" ")[0])
        return create_date_without_hour.replace(":", " ")

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")
        return 0

def find_related_files(jpg_file):
    """
    Troba els fitxers relacionats amb un fitxer JPG seleccionat.
    :param jpg_file: Nom del fitxer JPG seleccionat
    :return: Diccionari amb les rutes dels fitxers relacionats (HEIC, LIVE, MODIF).
    """

    # Ruta completa del fitxer JPG seleccionat
    jpg_file_basename = os.path.basename(jpg_file)
    jpg_file_basename_without_extension = os.path.splitext(jpg_file_basename)[0]
    jpg_file_parent_dir_path = os.path.dirname(jpg_file)

    # Inicialitzem el diccionari que retornarem
    related_files = {
        "JPG": {
            "BASENAME": jpg_file_basename,
            "RELATIVE_PATH": os.path.relpath(jpg_file_parent_dir_path,jpg_file_parent_dir_path),
            "SOURCE_ABS_PATH":os.path.abspath(jpg_file)
        }
    }

    # Ruta possible completa dels arxius relatius
    heic_file = os.path.join(jpg_file_parent_dir_path,"_HEIC",f"{jpg_file_basename_without_extension}.HEIC")
    live_file = os.path.join(jpg_file_parent_dir_path,"_MOV","_LIVE",f"{jpg_file_basename_without_extension}_LIVE.MOV")
    modif_file = os.path.join(jpg_file_parent_dir_path,f"{jpg_file_basename_without_extension}_MODIF.jpg")


    # Actualitzem el diccionari si existeixen els fitxers
    if os.path.exists(heic_file):
        related_files["HEIC"] = {
            "BASENAME" : os.path.basename(heic_file),
            "RELATIVE_PATH" : os.path.relpath(os.path.dirname(heic_file),jpg_file_parent_dir_path),
            "SOURCE_ABS_PATH":os.path.abspath(heic_file)
        }

    if os.path.exists(live_file):
        related_files["LIVE"] = {
            "BASENAME" : os.path.basename(live_file),
            "RELATIVE_PATH" : os.path.relpath(os.path.dirname(live_file),jpg_file_parent_dir_path),
            "SOURCE_ABS_PATH":os.path.abspath(live_file)

        }

    if os.path.exists(modif_file):
        related_files["MODIF"] = {
            "BASENAME" : os.path.basename(modif_file),
            "RELATIVE_PATH" : os.path.relpath(os.path.dirname(modif_file),jpg_file_parent_dir_path),
            "SOURCE_ABS_PATH":os.path.abspath(modif_file)
        }

    return related_files