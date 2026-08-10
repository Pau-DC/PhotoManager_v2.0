from pathlib import Path
import hashlib

## Hash parcial: incorpora la mida + fins a 'limit_bytes' del contingut.
def fast_hash(path: Path, limit_bytes=4 * 1024 * 1024, chunk_size=1024 * 1024):
    try:
        size = path.stat().st_size
    except FileNotFoundError:
        return None
    
    h = hashlib.blake2b(digest_size=16)
    h.update(size.to_bytes(8, "little", signed=False))
    with path.open("rb") as f:
        remaining = min(limit_bytes, size)
        while remaining > 0:
            chunk = f.read(min(chunk_size, remaining))
            if not chunk:
                break
            h.update(chunk)
            remaining -= len(chunk)
            
    return h.digest()


###Hash complet del fitxer (per confirmar coincidències).
def full_hash(path: Path, chunk_size=1024 * 1024):
    h = hashlib.blake2b(digest_size=32)
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.digest()
