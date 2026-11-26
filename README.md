# Vector Quantization

Lossy grayscale image compression and decompression using **Vector Quantization (VQ)** with the **LBG** codebook algorithm, written in Python.

Course assignment: *Information Theory & Data Compression*.

## How it works

### Compression
1. Read the image and convert it to grayscale.
2. Pad the image (edge replication) so its size is a multiple of the block size.
3. Split the image into blocks. Each block is one vector.
4. Build the codebook with the LBG algorithm (start from the mean, split every codeword, then refine).
5. Replace every block with the index of its nearest codeword.
6. Write the codebook file and the binary stream, then print the compression ratio.

### Decompression
1. Read the codebook file and the binary stream.
2. Replace every index with its codeword.
3. Rebuild the image and remove the padding.
4. Save the image as PNG.

The result is close to the original, not identical, because VQ is lossy.

## Project structure

```
vector_quantization/
├── __init__.py
├── main.py          # menu (compression / decompression)
├── compression.py   # vq_compression, vq_decompression, calculate_compression_ratio
├── vq_core.py       # padding, blocks, LBG codebook, nearest codeword
└── io_utils.py      # reading / writing images, codebook file and binary stream
```

## Requirements

- Python 3.8+
- NumPy
- Pillow

```
pip install numpy pillow
```

## Usage

Put the image in the same folder as `main.py`, then run:

```
python main.py
```

```
┌─────────────────────────┐
│ [ Vector Quantization ] │
├─────────────────────────┤
│  [1]  Compression       │
│  [2]  Decompression     │
│  [0]  Exit              │
└─────────────────────────┘
```

### Compression `[1]`

| Input | Example |
|---|---|
| Image name (with extension) | `1.jpeg` |
| Block height | `4` |
| Block width | `4` |
| Codebook size (number of vectors) | `64` |
| New file name | `new` |

Output:
- `new.bin`: the compressed image (binary stream of indices)
- `new_codebook.txt`: the codebook and the information needed for decompression

The compression ratio is printed after compression.

### Decompression `[2]`

| Input | Example |
|---|---|
| Compressed file name (without extension) | `new` |
| New image name | `out` |

Output: `out.png`

## Output files

**`name.bin`**: every block index written with `ceil(log2(codebook_size))` bits, packed into bytes. Extra zero bits are added to complete the last byte, and their count is saved in the codebook file.

**`name_codebook.txt`**: a Python dictionary stored as text containing:

| Key | Meaning |
|---|---|
| `height`, `width` | original image size |
| `padded_height`, `padded_width` | image size after padding |
| `block_h`, `block_w` | block size |
| `codebook_size` | number of codewords |
| `index_width` | bits used per index |
| `num_blocks` | number of blocks in the image |
| `extra_padding` | bits added to complete the last byte |
| `codebook` | the codewords (list of vectors) |

## Compression ratio

```
Compression Ratio = original size / (indices size + codebook size)

original size = height * width * 8
indices size  = num_blocks * index_width
codebook size = codebook_size * block_h * block_w * 8
```

All sizes are in bits.

## Notes

- Images are converted to grayscale (8 bits per pixel).
- The codebook size must be between 1 and the number of blocks in the padded image.
- Write the image name with its extension (for example `1.jpeg`). The compressed file name is written without extension.
