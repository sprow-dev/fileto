from PIL import Image
import os
import math
import sys
from tqdm import tqdm

def ftimg_main(inputp, chunksz=16384):
    print(f"Info: Read chunk size <{chunksz}>, Read file <{inputp}>")
    if not os.path.exists(inputp):
        print(f"File {inputp} not found. Is it in your current working directory and accessible?")
        print("Please note that file names are case sensitive.")
        return 1

    output = inputp + ".png"
    values = []
    size = os.path.getsize(inputp)
    print(f"Compiling <{size}> bytes of file <{inputp}>\n")

    try:
        with open(inputp, "rb") as b:
            with tqdm(total=size, unit="B", unit_scale=True, desc="Compiling bytes into list") as   progress:
                while True:
                    chunk = b.read(chunksz)
                    if not chunk:
                        print("\rFound EOF, final iteration.")
                        break
                    for byte in chunk:
                        values.append(byte)
                    progress.update(len(chunk))
    except Exception as e:
        print(f"Unhandled error <{e}> while compiling bytes")
        return

    lenvalues = len(values)
    imgsize = math.ceil(lenvalues / 3)
    side = int(math.ceil(math.sqrt(imgsize)))

    if (side * side) != imgsize:
        print("\nWarn: side values and image size are not equal. There will be white pixels at the end of the image.")

    print(f"Creating <{side}x{side}> image with <{imgsize}> pixels\n")

    image = Image.new("RGB", (side, side), color="black")
    draw = image.load()

    # b = progress bar
    for b in tqdm(range(imgsize), unit="Px", unit_scale=True, desc=f"Drawing pixels to image"):
        b3 = b*3
        if b3+2 >= lenvalues:
            break

        draw[b%side,b//side] = (values[b3],values[b3+1],values[b3+2])

    try:
        image.save(output)
        print(f"\nSaved image <{output}> to disk.")
    except Exception as e:
        print(f"Unhandled error <{e}> while writing to disk.")

    print(f"Completed. Produced file <{output}> with <{imgsize}> pixels as a <{side}x{side}> color PNG.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an argument.")
        print("Example usage: python3 ftimg.py song.wav")
        sys.exit(1)

    inputp = sys.argv[1]
    ftimg_main(inputp)
