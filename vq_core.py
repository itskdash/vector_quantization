import numpy as np

def pad_image(image, block_h, block_w):
    height, width = image.shape
    pad_h = (-height) % block_h
    pad_w = (-width) % block_w

    return np.pad(image, ((0, pad_h), (0, pad_w)), mode="edge")

def image_to_blocks(image, block_h, block_w):
    blocks = []

    for i in range(0, image.shape[0], block_h):
        for j in range(0, image.shape[1], block_w):
            blocks.append(image[i:i + block_h, j:j + block_w].flatten())

    return np.array(blocks, dtype=float)

def blocks_to_image(blocks, height, width, block_h, block_w):
    image = np.zeros((height, width))
    index = 0

    for i in range(0, height, block_h):
        for j in range(0, width, block_w):
            image[i:i + block_h, j:j + block_w] = blocks[index].reshape(block_h, block_w)
            index += 1

    return image

def find_nearest(vectors, codebook):
    distances = (
        (vectors ** 2).sum(axis=1)[:, None]
        - 2 * vectors @ codebook.T
        + (codebook ** 2).sum(axis=1)
    )

    return distances.argmin(axis=1)

def build_codebook(vectors, codebook_size):
    codebook = vectors.mean(axis=0, keepdims=True)

    while len(codebook) < codebook_size:
        codebook = np.vstack([codebook * 1.001, codebook * 0.999])

        for _ in range(20):
            indices = find_nearest(vectors, codebook)

            for c in range(len(codebook)):
                group = vectors[indices == c]

                if len(group) > 0:
                    codebook[c] = group.mean(axis=0)
                else:
                    codebook[c] = vectors[np.random.randint(len(vectors))]

    return codebook[:codebook_size]