import datetime
import os
from commons.hash_operations import *
from pathlib import Path


##### indexing & search #####
# Itera tots els fitxers sota 'root'. Ignora enllaços simbòlics.
def iter_files(root: Path):
    for dirpath, _, filenames in os.walk(root):
        d = Path(dirpath)
        for name in filenames:
            p = d / name
            try:
                if not p.is_symlink() and p.is_file():
                    yield p
            except Exception:
                # permisos, fitxers desapareguts, etc.
                continue

# Crea un índex {(mida, fast_hash) -> [paths...]} per a la carpeta destí.
def index_target(dest_root: Path):
    index = {}
    total = 0
    for p in iter_files(dest_root):
        try:
            size = p.stat().st_size
            fh = fast_hash(p)
            if fh is None:
                continue
            key = (size, fh.hex())

            print(f"[DEBUG] Checking {p.name} size={size} fh={fh.hex()}")

            index.setdefault(key, []).append(p)
            total += 1
        except Exception:
            continue
    return index, total

# Retorna True si hi ha un fitxer idèntic a dest (mateix hash complet)."""
def exists_in_dest_by_content(src_file: Path, fast_index):
    try:
        size = src_file.stat().st_size
    except Exception as e:
            # General exception handling
        print(f"An error occurred: {e}")
        return False
    except FileNotFoundError:
        return False
    
    fh = fast_hash(src_file)
    if fh is None:
        return False
    
    key = (size, fh.hex())

    candidates = fast_index.get(key, [])

    print(f"[DEBUG] Checking {src_file.name} size={size} fh={fh.hex()} candidates={len(candidates)}")
    
    if not candidates:
        return False
    
    # confirmació amb hash complet
    src_full = full_hash(src_file)
    for c in candidates:
        try:
            if full_hash(c) == src_full:
                return True
        except Exception as e:
            # General exception handling
            print(f"An error occurred: {e}")
            return False
        except Exception:
            continue
    
    return False

# Funció que compara les carpetes
def indexing_target_folder(target_folder):

    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Indexing files in folder {target_folder}")

        # Creem un índex amb els arxius de la carpeta target
        fast_index, total_dest = index_target(target_folder)

    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")
        return False

    finally:
        # Extraiem el resultat i retornem l'índex
        print(f"\t |-- Execution complete in {datetime.datetime.now()-initial_time} ms.")
        print(f"\t |-- Files indexed on target folder: {total_dest}")

        return fast_index

def compare_folders(original_folder, fast_index):

    try:
        # Inicialització de la variable de temps
        initial_time = datetime.datetime.now()
        print(f"\t + [{initial_time}] Comparing files from folder {original_folder}")

        # Inicialitzem les variables
        duplicates = 0
        duplicates_collection = [] 
        news = 0
        news_collection = []
        total_src = 0


        # Per tots els fitxers continugts a la carpeta d'origen
        for p in iter_files(original_folder):
            total_src += 1
            try:
                # Comprovem si hi ha un fitxer existens en l'índex creat anteriorment amb els fitxers de la carpeta destí
                found = exists_in_dest_by_content(p, fast_index)

                # Actualitzem els valors
                if found:
                    duplicates += 1
                    duplicates_collection.append(p) 
                else:
                    news += 1
                    news_collection.append(p)

            except Exception as e:
                print(f"[ERROR] {p}: {e}")
                continue
    except Exception as e:
        # General exception handling
        print(f"An error occurred: {e}")
        return False
    
    finally:
        print(f"\t |-- Fitxers analitzats : {total_src}")
        print(f"\t |-- Duplicats          : {duplicates}")
        print(f"\t |-- Nous               : {news}")

        return duplicates_collection, news_collection
