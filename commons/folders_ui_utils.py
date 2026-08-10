import tkinter as tk
from tkinter import filedialog
from commons.folders_utils import *
from AppKit import NSOpenPanel


#def select_folder(title=""):
#    root = tk.Tk()
#    root.withdraw()  # Oculta la finestra principal
#    return filedialog.askdirectory(title=title)

def select_folder(title="Selecciona una carpeta"):
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(False)
    panel.setCanChooseDirectories_(True)
    panel.setAllowsMultipleSelection_(False)
    panel.setTitle_(title)

    if panel.runModal():
        return panel.URLs()[0].path()
    return None


def select_folders_from_parent(parent=""):
  if parent == "":
    parent = select_folder(
       title="Selecciona la carpeta principal que conté les carpetes a fusionar" 
    )
  return subfolders_list(parent)