
import json
import os
import numpy as np
from PIL import Image


def read_image(filename):
    if not os.path.isfile(filename):
        return None

    try:
        image = Image.open(filename)

        if image.mode == "L":
            return np.array(image, dtype=np.uint8)

        image = image.convert("RGB")
        return np.array(image, dtype=np.uint8)

    except (OSError, ValueError):
        return None


def write_image(image_array, filename):
    image_array = np.asarray(image_array)
    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    if image_array.ndim == 2:
        image = Image.fromarray(image_array, mode="L")
    elif image_array.ndim == 3 and image_array.shape[2] == 3:
        image = Image.fromarray(image_array, mode="RGB")
    else:
        raise ValueError("Image must be grayscale or RGB.")

    image.save(filename)


def convert_to_json(value):
    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    if isinstance(value, dict):
        return {
            key: convert_to_json(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [convert_to_json(item) for item in value]

    return value


def get_file_names(filename):
    if filename.lower().endswith(".bin"):
        filename = filename[:-4]

    binary_file = filename + ".bin"
    codebook_file = filename + "_codebook.json"

    return binary_file, codebook_file


def write_vq_compressed(bitstream, metadata, filename):
    binary_file, codebook_file = get_file_names(filename)

    if not isinstance(bitstream, str):
        raise TypeError("bitstream must be a string of 0s and 1s.")

    if any(bit not in "01" for bit in bitstream):
        raise ValueError("bitstream must contain only 0s and 1s.")

    metadata = dict(metadata)

    extra_padding = (8 - len(bitstream) % 8) % 8
    padded_bitstream = bitstream + ("0" * extra_padding)

    metadata["extra_padding"] = extra_padding

    byte_array = bytearray()

    for i in range(0, len(padded_bitstream), 8):
        byte = padded_bitstream[i:i + 8]
        byte_array.append(int(byte, 2))

    with open(binary_file, "wb") as file:
        file.write(byte_array)

    with open(codebook_file, "w", encoding="utf-8") as file:
        json.dump(convert_to_json(metadata), file)


def read_vq_compressed(filename):
    binary_file, codebook_file = get_file_names(filename)

    if not os.path.isfile(binary_file) or not os.path.isfile(codebook_file):
        return None, None

    try:
        with open(binary_file, "rb") as file:
            bytes_data = file.read()

        with open(codebook_file, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        bitstream = "".join(f"{byte:08b}" for byte in bytes_data)

        extra_padding = metadata.get("extra_padding", 0)

        if extra_padding > 0:
            bitstream = bitstream[:-extra_padding]

        return bitstream, metadata

    except (OSError, json.JSONDecodeError, ValueError):
        return None, None
