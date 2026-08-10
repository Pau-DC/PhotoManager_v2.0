from commons.files_utils import *

def process_photos_from_iphone(masters_folder, edits_folder=""):
    #Modifiquem totes les extensions per passar-les a majúscules
    uppercase_files_extension(masters_folder)

    # Identifiquem els arxius LIVE i els anomenem segons el seu HEIC associat
    identify_lives(masters_folder)

    # Modifiquem el títol de l'arxiu d'aquells heic que puguin ser retrats o fotos modificades i els movem a la carpeta Master
    if edits_folder != "":
       identify_modifs_in_edits_folder(masters_folder, edits_folder)
    else:
       identify_modifs(masters_folder)

    # Convertim tots els arxius HEIC a JPG
    convert_HEIC_to_JPG(masters_folder)

    # Modifiquem el títol de l'arxiu d'aquells mov que puguin ser SlowMotion
    identify_slowmotion(masters_folder)

    # Modifiquem el títol de l'arxiu d'aquells mov que puguin ser TimeLapse
    identify_timelapse(masters_folder)

    # Actualitzem les dates dels arxius de la carpeta a la data de creació de la foto
    update_files_dates_from_folder(masters_folder)