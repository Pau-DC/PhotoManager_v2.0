from commons.folders_ui_utils import select_folder


def check_args_if_folder_and_return_path(path_folder, folder_title):
    # Comprovem si s'han passat els arguments de la carpeta
    if path_folder:
        # Comprovem si és un path del tipus carpeta
        if not path_folder.is_dir():
            raise Exception(f"Not a folder: {path_folder}")
        return path_folder
    else:
        # Si no s'ha passat argument, seleccionem de carpeta mitjançant interfícies gràfica
        return select_folder(folder_title)
        
    