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

                    # OLD METHOD
                    # # Per cada fitxer creat preparem la comanda fent ús d'ExifTool i subprocess 
                    # # ja que no és una llibreria nativa de Python
                    # comand = f"exiftool -tagsFromFile {os.path.join(masters_folder,file_basename_without_extension)}.HEIC -all:all -FileCreateDate -FileModifyDate -Orientation=1 -n -overwrite_original {os.path.join(masters_folder,file_basename_without_extension)}.JPG"
                    # result = subprocess.run(comand, stdout=subprocess.PIPE, text=True)    

                    # # Llencem una exepció si hi ha hagut error en l'execució
                    # if result.returncode != 0:
                    #      # Llançar una excepció si hi ha un error
                    #      raise subprocess.CalledProcessError(result.returncode, comand, output=result.stdout, stderr=result.stderr)
                    
                    # # Obtenim el nombre d'imatges convertides
                    # match = re.search(r"(\d+) image files updated", result.stdout)

                    # if match:
                    #     num_converted_files += int(match.group(1))
                    # else:
                    #     num_converted_files += 0

                    # NEW METHOD
                    # Executem la comanda d'exiftool i en tractem el resultat
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

         # Preparem les variables dels arxius que contenen la carpeta actual
        files = files_list(masters_folder)
        num_slowmotion_files = 0 

         # Per tots els arxius
        for file in files:

            # Preparem les variables necessàries
            file_basename = os.path.basename(file)
            file_basename_without_extension = os.path.splitext(file_basename)[0]
            framerate_limit = 60

            # Per cada fitxer tipus MOV
            # if file.lower().endswith(".mov"):

                #Comparem el framerate de l'arxiu amb el límit que hem definit per diferenciar-ne els slowmotions


    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")

    finally:
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- {num_slowmotion_files} files identifyied as lives")

def update_files_dates_from_folder(masters_folder):
    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Updating dates from files in {masters_folder}...")

        # Deprecated method: s'ha deprecat la modificació dels arxius un a un per eficiència
                # # Preparem les variables dels arxius que contenen la carpeta actual
                # files = files_list(masters_folder)
                # subfolders = subfolders_list(masters_folder)
                # num_updated_files = 0 


                # # Per tots els arxius dins de la carpeta...
                # for file in files:
                    
                #     # ... actualitzem la data a la data de creació de la foto
                #     num_updated_files += update_file_dates_from_file(file)

        # Preparem les variables dels arxius que contenen la carpeta actual
        num_updated_files = 0 

        # OLD METHOD
        # # Preparem la comanda fent ús d'ExifTool i subprocess 
        # # ja que no és una llibreria nativa de Python
        # comand = f"exiftool -m \"-FileCreateDate<createDate\" \"-FileModifyDate<createDate\" -ext jpg -ext heic \"-FileCreateDate<creationDate\" \"-FileModifyDate<creationDate\" -ext mov \"-FileCreateDate<DateTimeOriginal\" \"-FileModifyDate<DateTimeOriginal\" -ext png {masters_folder}"
        # result = subprocess.run(comand, stdout=subprocess.PIPE, text=True)    

        # # # Llencem una exepció si hi ha hagut error en l'execució
        # if result.returncode != 0:
        #      # Llançar una excepció si hi ha un error
        #      raise subprocess.CalledProcessError(result.returncode, comand, output=result.stdout, stderr=result.stderr)
        
        # # Obtenim el nombre d'imatges actualitzades
        # match = re.search(r"(\d+) image files updated", result.stdout)

        # if match:
        #     num_updated_files = int(match.group(1))
        # else:
        #     num_updated_files = 0

        # NEW METHOD
        # Executem la comanda d'exiftool i en tractem el resultat
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


        # OLD METHOD
        # Per cada arxiu apliquem la comanda fent ús de ExifTool i subprocess 
        # # ja que no és una llibreria nativa de Python
        # comand = f"exiftool \"-FileCreateDate<{original_date}\" \"-FileModifyDate<{original_date}\" {file}"
        # result = subprocess.run(comand, capture_output=True, text=True)

        # # Llencem una exepció si hi ha hagut error en l'execució
        # if result.returncode != 0:
        #     # Llançar una excepció si hi ha un error
        #     raise subprocess.CalledProcessError(result.returncode, comand, output=result.stdout, stderr=result.stderr)
        # else:
        #     return 1


        # NEW METHOD
        # Executem la comanda d'exiftool i en tractem el resultat
        result = exectue_comand(f"exiftool \"-FileCreateDate<{original_date}\" \"-FileModifyDate<{original_date}\" {file}")
        num_updated_files += extract_int_from_output(result, "image files updated")


    except subprocess.CalledProcessError as e:
        # Gestionar l'error: mostrar l'error i la sortida stderr
        print(f"Error executing ExifTool: {e.stderr}")
        return 0

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")
        return 0


