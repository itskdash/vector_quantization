from io_utils import (
    read_image,
    write_image,
    read_vq_compressed,
    write_vq_compressed
)
from compression import (
    vq_compression,
    vq_decompression,
    calculate_compression_ratio
)

def run_app():
    print(
        "\n┌─────────────────────────┐"
        "\n│       | Welcome |       │"
        "\n│  Data Compression App   │"
        "\n└─────────────────────────┘"
    )

    while True:
        print(
            "\n┌─────────────────────────┐"
            "\n│ [ Vector Quantization ] │"
            "\n├─────────────────────────┤"
            "\n│  [1]  Compression       │"
            "\n│  [2]  Decompression     │"
            "\n│  [0]  Exit              │"
            "\n└─────────────────────────┘"
        )

        try:
            choice = int(input("Please enter your choice: "))

            if choice == 1:
                filename = input("Please enter image name (with extension): ").strip()
                image = read_image(filename)

                if image is None:
                    print("File not found please enter a valid file name.")
                else:
                    block_h = int(input("Please enter block height: "))
                    block_w = int(input("Please enter block width: "))
                    codebook_size = int(input("Please enter codebook size: "))

                    bitstream, metadata = vq_compression(image, block_h, block_w, codebook_size)
                    newname = input("Enter new file name: ").strip()
                    write_vq_compressed(bitstream, metadata, newname)

                    print("File created successfully!")
                    print("Compressed file:", newname + ".bin")
                    print("Codebook file:", newname + "_codebook.txt")
                    print(f"Compression ratio: {calculate_compression_ratio(metadata):.2f}")

            elif choice == 2:
                filename = input("Please enter compressed file name: ").strip()
                bitstream, metadata = read_vq_compressed(filename)

                if bitstream is None or metadata is None:
                    print("File not found please enter a valid file name.")
                else:
                    image = vq_decompression(bitstream, metadata)
                    newname = input("Enter new image name: ").strip()
                    write_image(image, newname)
                    print("Image decompressed successfully!")
                    print("Image file:", newname + ".png")

            elif choice == 0:
                print("\nGoodbye!")
                break

            else:
                print("Invalid choice please try again.")

        except (ValueError, SyntaxError, KeyError, TypeError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_app()