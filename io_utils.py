import os
import ast
import numpy as np
from PIL import Image

def read_image(filename):
    folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(folder, filename)

    try:
        return np.array(Image.open(filepath).convert("L"))

    except OSError:
        return None

def write_image(image, newname):
    folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(folder, newname + ".png")

    Image.fromarray(image).save(filepath)

def read_vq_compressed(filename):
    folder = os.path.dirname(os.path.abspath(__file__))
    bitstream_path = os.path.join(folder, filename + ".bin")
    codebook_path = os.path.join(folder, filename + "_codebook.txt")

    try:
        with open(codebook_path, "r", encoding="utf-8") as file:
            metadata = ast.literal_eval(file.read())

        with open(bitstream_path, "rb") as file:
            bytes_data = file.read()

        bitstream = "".join(f"{byte:08b}" for byte in bytes_data)

        extra_padding = metadata.get("extra_padding", 0)
        if extra_padding > 0:
            bitstream = bitstream[:-extra_padding]

        return bitstream, metadata

    except FileNotFoundError:
        return None, None

def write_vq_compressed(bitstream, metadata, newname):
    folder = os.path.dirname(os.path.abspath(__file__))
    bitstream_path = os.path.join(folder, newname + ".bin")
    codebook_path = os.path.join(folder, newname + "_codebook.txt")

    extra_padding = (8 - len(bitstream) % 8) % 8
    bitstream += "0" * extra_padding

    metadata["extra_padding"] = extra_padding

    byte_array = bytearray()
    for i in range(0, len(bitstream), 8):
        byte = bitstream[i:i + 8]
        byte_array.append(int(byte, 2))

    with open(bitstream_path, "wb") as file:
        file.write(byte_array)

    with open(codebook_path, "w", encoding="utf-8") as file:
        file.write(repr(metadata))