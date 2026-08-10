import datetime
import subprocess
import re
import pillow_heif
from commons.folders_utils import *
from commons.common_utils import *
from PIL import Image


def identify_lives(masters_folder):

    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying lives from files in {masters_folder}...")

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
        print(f"\t + [{initial_time}] Identifying modified files from files in {masters_folder}...")

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

        # Si la carpeta EDITS està buida l'eliminem
        if not os.listdir(edits_folder):
            os.rmdir(edits_folder)

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
        print(f"\t + [{initial_time}] Identifying modified files from files in {masters_folder}...")

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
        print(f"\t + [{initial_time}] Converting HEIC files to JPG in {masters_folder}...")

         # Preparem les variables dels arxius que contenen la carpeta actual
        files = files_list(masters_folder)
        num_converted_files = 0 

        # Per tots els arxius
        for file in files:

            # Preparem les variables necessàries
            file_basename = os.path.basename(file)
            file_basename_without_extension = os.path.splitext(file_basename)[0]

            # Per cada fitxer tipus HEIC el convertim a JPG
            if file.lower().endswith(".heic"):
                    heif_file = pillow_heif.open_heif(file)
                    image = Image.frombytes(
                        heif_file.mode, 
                        heif_file.size, 
                        heif_file.data,
                    )
                    image.save(os.path.join(masters_folder,file_basename_without_extension+".JPG"), "JPEG")

                    # Per cada fitxer creat preparem la comanda fent ús d'ExifTool i en tractem el resultat
                    result = exectue_comand(f"exiftool -tagsFromFile {os.path.join(masters_folder,file_basename_without_extension)}.HEIC -all:all -FileCreateDate -FileModifyDate -Orientation=1 -n -overwrite_original {os.path.join(masters_folder,file_basename_without_extension)}.JPG")
                    num_converted_files += extract_int_from_output(result, "image files updated")

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_converted_files} updated files")

def identify_slowmotion(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Identifying slowmotion from files in {masters_folder}...")

        # Preparem les variables globals de la funció
        framerate_limit = 60
        num_slowmotion_files = 0 

#  PER INVESTIGAR SI PUC OPTIMITZAR EL BUCLE I EL CONDICIONAL DE FRAMERATE ALHORA
        

        # # Preparem les variables dels arxius que contenen la carpeta actual
        # files = files_list(masters_folder)

         # Per tots els arxius
        # for file in files:

        #     # Preparem les variables necessàries
        #     file_basename = os.path.basename(file)
        #     file_basename_without_extension = os.path.splitext(file_basename)[0]

            # # Per cada fitxer tipus MOV
            # if file.lower().endswith(".mov"):

            #     # Extraiem la metadata frame rate 
            #     result = exectue_comand(f"exiftool -s3 -VideoFrameRate {file}")
            #     framerate_extracted = float(result.strip())

            #     if framerate_extracted > framerate_limit:
            #         # Renombrem el nom del fitxer afegint el sufix "_SLOWMOTION"
            #         os.rename(file,os.path.join(masters_folder,file_basename_without_extension+"_SLOWMOTION.MOV"))
            #         num_slowmotion_files += 1

        result = exectue_comand(f"exiftool -s3 -n -if \"$FileType eq \'MOV\' and $VideoFrameRate > {framerate_limit}\" -p \"$FilePath\" -m -q -q {masters_folder}")
        files = result.splitlines()

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
        print(f"\t + [{initial_time}] Identifying timelapse from files in {masters_folder}...")

        # Preparem les variables globals de la funció
        num_timelapse_files = 0 

#  PER INVESTIGAR SI PUC OPTIMITZAR EL BUCLE I EL CONDICIONAL DE FRAMERATE ALHORA

        #  # Preparem les variables dels arxius que contenen la carpeta actual
        # files = files_list(masters_folder)

        #  # Per tots els arxius
        # for file in files:

        #     # Preparem les variables necessàries
        #     file_basename = os.path.basename(file)
        #     file_basename_without_extension = os.path.splitext(file_basename)[0]
        #     framerate_limit = 60

        #     # Per cada fitxer tipus MOV
        #     if file.lower().endswith(".mov"):

        #         # Extraiem la metadata frame rate 
        #         result = exectue_comand(f"exiftool -m -s3 -capturemode {file}")

        #         if result == "Time-lapse":
        #             # Renombrem el nom del fitxer afegint el sufix "_TIMELAPSE"
        #             os.rename(file,os.path.join(masters_folder,file_basename_without_extension+"_TIMELAPSE.MOV"))
        #             num_timelapse_files += 1

        result = exectue_comand(f"exiftool -s3 -n -if \"$FileType eq \'MOV\' and $capturemode eq \'Time-lapse\'\" -p \"$FilePath\" -m -q -q {masters_folder}")
        files = result.splitlines()

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
        print(f"\t + [{initial_time}] Updating dates from files in {masters_folder}...")

        # Preparem les variables dels arxius que contenen la carpeta actual
        num_updated_files = 0 

        # Preparem la comanda fent ús d'ExifTool i en tractem el resultat
        result = exectue_comand(f"exiftool -m \"-FileCreateDate<createDate\" \"-FileModifyDate<createDate\" -ext jpg -ext heic \"-FileCreateDate<creationDate\" \"-FileModifyDate<creationDate\" -ext mov \"-FileCreateDate<DateTimeOriginal\" \"-FileModifyDate<DateTimeOriginal\" -ext png {masters_folder}")
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
        result = exectue_comand(f"exiftool \"-FileCreateDate<{original_date}\" \"-FileModifyDate<{original_date}\" {file}")
        num_updated_files += extract_int_from_output(result, "image files updated")

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")
        return 0