#!/bin/bash

# Accedim i activem l'entorn virtual
cd /volume1/dateutil_env/
source bin/activate

# Actualitzem el Path per a que hi inclogui la carpeta de binaris d'Exiftool
export PATH=$PATH:/usr/share/applications/ExifTool

# Cridem l'script de Python que inciarà tot el procés de gestió de fotografies
python3 /volume1/homes/NAS_PA_ADMIN/Scripts/PhotoManager_v2.0/PhotoManager_2.0_SynologyScript.py
#python3 /volume1/homes/NAS_PA_ADMIN/Scripts/PhotoManager_v2.0/PhotoManager_2.0.py 
#    --masters "/volume1/homes/NAS_PA_ADMIN/Photos_Manager/1_To_Process/"
#    --destination "/volume1/homes/NAS_PA_ADMIN/Photos_Manager/3_To_Move/"
#    --output "/volume1/Scripts_outputs/Photos_Manager_Scripts_outputs"
