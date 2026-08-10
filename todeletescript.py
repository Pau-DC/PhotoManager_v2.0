from pathlib import Path
from commons.hash_operations import *

def first_bytes(path, n=64):
    with open(path, 'rb') as f:
        return f.read(n)

f1 = Path("/Users/paudomigo/Desktop/_TO_TEST_SCRIPT_TARGET/2025 03 01 _ Rua del carnaval infantil de Sants/IMG_8957.JPG")
f2 = Path("/Users/paudomigo/Desktop/_TO_TEST_SCRIPT/2_NewFiles/IMG_8957_2.JPG")

def first_diff_byte(path1, path2):
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        offset = 0
        while True:
            b1 = f1.read(1)
            b2 = f2.read(1)
            if not b1 or not b2:
                return None  # iguals fins al final
            if b1 != b2:
                return offset, b1, b2
            offset += 1

fh_f1 = fast_hash(f1)
fh_f2 = fast_hash(f2)

print(len(first_bytes(f1, 64)))
print(first_bytes(f1, 64))
print(first_bytes(f2, 64))
print(fh_f1.hex())
print(fh_f2.hex())


diff = first_diff_byte(f1, f2)

print("Primera diferència:", diff)

