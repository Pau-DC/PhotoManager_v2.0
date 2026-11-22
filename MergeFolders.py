"""
MergeFolders
------------
Fusiona dues o més carpetes de fotos dins de la de data més antiga.

Ús:
  python3 MergeFolders.py <carpeta1> <carpeta2> [...]          (des d'Automator: botó dret sobre les carpetes)
  python3 MergeFolders.py --dry-run <carpeta1> <carpeta2> ...  (simulació: mostra què faria sense moure res)
  python3 MergeFolders.py --yes <carpeta1> <carpeta2> ...      (sense diàleg de confirmació)

Log de cada execució: ~/Library/Logs/PhotoManager/AAAAMMDDhhmmss_MergeFolders.log
"""

import datetime
import os
import sys
import traceback
from commons.mac_utils import ScriptLog, notify, confirm_dialog
from commons.merge_utils import validate_folders, choose_target_folder, merge_folders_by_date

initial_time = datetime.datetime.now()
log = ScriptLog("MergeFolders")

args = sys.argv[1:]
dry_run = "--dry-run" in args
skip_confirm = "--yes" in args
folders = [a for a in args if a not in ("--dry-run", "--yes")]

try:
    print(f"[{initial_time}] - Initializating process...{' (SIMULACIÓ)' if dry_run else ''}")
    print(f"Arguments rebuts: {folders}")

    folders = validate_folders(folders)
    target, sources = choose_target_folder(folders)

    print(f"Carpeta destí (la més antiga): {target}")
    for s in sources:
        print(f"  + {s}")

    # Confirmació abans de moure res
    if not dry_run and not skip_confirm:
        names = "\n".join(f"   • {os.path.basename(s)}" for s in sources)
        message = (f"Es fusionaran {len(sources)} carpeta(es) dins de:\n\n   {os.path.basename(target)}\n\n"
                   f"Carpetes que s'eliminaran un cop buides:\n{names}")
        if not confirm_dialog(message, title="MergeFolders", ok_button="Fusiona"):
            print("Cancel·lat per l'usuari. No s'ha mogut res.")
            notify("MergeFolders", "Cancel·lat. No s'ha mogut res.")
            sys.exit(0)

    target, stats = merge_folders_by_date(folders, dry_run)

    summary = (f"{stats['moved']} moguts, {stats['renamed']} reanomenats, "
               f"{stats['duplicates']} duplicats eliminats, {stats['errors']} errors")
    print(f"\nResum: {summary}")

    if dry_run:
        print("SIMULACIÓ: no s'ha modificat cap fitxer.")
    elif stats["errors"] or stats["not_empty"]:
        notify("MergeFolders ⚠️", f"{summary}. Mira el log a ~/Library/Logs/PhotoManager")
    else:
        notify("MergeFolders ✅", f"Fusionat a '{os.path.basename(target)}': {summary}")

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    notify("MergeFolders ⚠️", f"Error: {e}")

finally:
    print(f"\n[{datetime.datetime.now()}] Execution complete in {datetime.datetime.now()-initial_time} ms.")
    print(f"Log: {log.path}")
    log.close()