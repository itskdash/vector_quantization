from io_utils import (
    read_image,
    write_image,
    read_vq_compressed,
    write_vq_compressed
)
from compression import (
    vq_compression,
    vq_decompression,
    compression_ratio
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
            "\n│  [ Vector Quantization ]│"
            "\n├─────────────────────────┤"
            "\n│  [1]  Compression       │"
            "\n│  [2]  Decompression     │"
            "\n│  [0]  Exit              │"
            "\n└─────────────────────────┘"
        )

        try:
            choice = int(input("Please enter your choice: "))

            if choice == 1:
                filename = input("Please enter image name: ").strip()
                img = read_image(filename)

                if img is None:
                    print("File not found please enter a valid file name.")
                else:
                    bh = int(input("Block height: "))
                    bw = int(input("Block width: "))
                    k = int(input("Codebook size (number of vectors): "))

                    bitstream, metadata = vq_compression(img, bh, bw, k)
                    newname = input("Enter new file name: ").strip()
                    write_vq_compressed(bitstream, metadata, newname)

                    print("File created successfully!")
                    print("Compressed file:", newname + ".bin")
                    print("Codebook file:", newname + "_codebook.json")
                    print(f"Compression ratio: {compression_ratio(metadata):.2f}")

            elif choice == 2:
                filename = input("Please enter compressed file name: ").strip()
                bitstream, metadata = read_vq_compressed(filename)

                if bitstream is None or metadata is None:
                    print("File not found please enter a valid file name.")
                else:
                    img = vq_decompression(bitstream, metadata)
                    newname = input("Enter new image name (e.g. out.png): ").strip()
                    write_image(img, newname)
                    print("Image decompressed successfully!")

            elif choice == 0:
                print("\nGoodbye!")
                break

            else:
                print("Invalid choice please try again.")

        except (ValueError, SyntaxError, KeyError, TypeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    run_app()