#!/bin/bash
#
# wrapper.sh
# ------------------------------------------------------------------
# Punt d'entrada del procés nocturn de gestió de fotos de l'iPhone.
# Invocat automàticament cada nit a les 3:30h per una tasca del
# Task Scheduler (Panell de control > Programador de tasques) del
# Synology, amb la comanda:
#   chmod +x wrapper.sh && ./wrapper.sh
#
# Fa 3 coses:
#   1. Activa l'entorn virtual Python amb les dependències necessàries
#      (Pillow, pillow_heif, etc.)
#   2. Afegeix ExifTool al PATH (necessari per llegir/escriure metadades)
#   3. Executa PhotoManager_2.0_SynologyScript.py, que processa
#      1_To_Process/ i mou el resultat a 3_To_Move/
#
# Logs de cada execució: /volume1/Scripts_outputs/Photos_Manager_Scripts_outputs/
# ------------------------------------------------------------------

set -euo pipefail  # Atura l'script si falla qualsevol comanda

VENV_PATH="/volume1/dateutil_env"
SCRIPT_PATH="/volume1/homes/NAS_PA_ADMIN/Scripts/PhotoManager_v2.0/PhotoManager_2.0_SynologyScript.py"
EXIFTOOL_PATH="/usr/share/applications/ExifTool"

# Accedim i activem l'entorn virtual
cd "$VENV_PATH" || { echo "ERROR: no es pot accedir a $VENV_PATH"; exit 1; }
source bin/activate || { echo "ERROR: no s'ha pogut activar l'entorn virtual"; exit 1; }

# Actualitzem el PATH per incloure els binaris d'ExifTool
export PATH="$PATH:$EXIFTOOL_PATH"

# Executem el script principal
python3 "$SCRIPT_PATH"