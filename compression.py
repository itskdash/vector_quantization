import math
import numpy as np
from vq_core import (
    pad_image,
    image_to_blocks,
    blocks_to_image,
    build_codebook,
    find_nearest
)

def vq_compression(image, block_h, block_w, codebook_size):
    height, width = image.shape

    padded = pad_image(image, block_h, block_w)
    vectors = image_to_blocks(padded, block_h, block_w)

    if codebook_size < 1 or codebook_size > len(vectors):
        raise ValueError(f"Codebook size must be between 1 and {len(vectors)}")

    codebook = build_codebook(vectors, codebook_size)
    indices = find_nearest(vectors, codebook)

    index_width = max(1, math.ceil(math.log2(codebook_size)))

    bitstream = ""
    for index in indices:
        bitstream += format(int(index), f"0{index_width}b")

    metadata = {
        "height": height,
        "width": width,
        "padded_height": padded.shape[0],
        "padded_width": padded.shape[1],
        "block_h": block_h,
        "block_w": block_w,
        "codebook_size": codebook_size,
        "index_width": index_width,
        "num_blocks": len(indices),
        "codebook": np.round(codebook).astype(int).tolist()
    }

    return bitstream, metadata

def vq_decompression(bitstream, metadata):
    index_width = metadata["index_width"]
    codebook = np.array(metadata["codebook"])

    if len(bitstream) != metadata["num_blocks"] * index_width:
        raise ValueError("Invalid bitstream length")

    indices = []
    for i in range(0, len(bitstream), index_width):
        index = int(bitstream[i:i + index_width], 2)

        if index >= len(codebook):
            raise ValueError("Invalid codebook index")

        indices.append(index)

    image = blocks_to_image(
        codebook[indices],
        metadata["padded_height"],
        metadata["padded_width"],
        metadata["block_h"],
        metadata["block_w"]
    )

    image = image[:metadata["height"], :metadata["width"]]

    return np.clip(image, 0, 255).astype(np.uint8)

def calculate_compression_ratio(metadata):
    original_size = metadata["height"] * metadata["width"] * 8
    indices_size = metadata["num_blocks"] * metadata["index_width"]
    codebook_size = metadata["codebook_size"] * metadata["block_h"] * metadata["block_w"] * 8

    return original_size / (indices_size + codebook_size)