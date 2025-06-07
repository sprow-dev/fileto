import numpy as np
import soundfile as sf
from tqdm.auto import tqdm
import os
import sys

def ftaud_audio(values:list[int],
                output:str,
                rate:int=44100,
                channels:int=2,
                vol:float=0.5,
                chunksz=16384,
                audioformat:str="r") -> str:
    """
    values: input a list of data in the format "bytes"
    output: filename of the output file
    rate: sample rate of the ftaud_audio such as 44100 (default)
    channels: how many channels there are, 1 for mono and 2 (default) for stereo are the only values currently supported
    normalized: True (default) and False are the supported values
    vol: volume as a float from 0 to 1
    chunksz: the write chunk size
    """
    if audioformat == "c":
        stype="VORBIS"
    else:
        stype="FLOAT"
    if not values:
        print("No bytes found. Did you provide an empty file?")
        sys.exit(1)
    if not (0.0 <= vol <= 1.0):
        print("Clamping volume to closest valid number.")
        vol = max(0.0, min(1.0, vol))


    try:
        data = np.array(values, dtype=np.float32)

        if channels == 1 and data.ndim == 1:
            data = data.reshape(-1, 1)
        elif channels > 1 and data.shape[0] % channels == 0:
            data = data.reshape(-1, channels)
        else:
            return f"Data ({data.shape[0]}) incompatible with {channels} channels."

        data = data * vol
        samples = data.shape[0]
        sample_chunk_size = max(1, chunksz // (4 * channels))

        print(f"\nWriting data for {output}")
        with sf.SoundFile(output, 'w', rate, channels, stype) as f:
            with tqdm(total=samples, unit="Chunk", unit_scale=True, desc="Writing data") as progress:
                for i in range(0, samples, sample_chunk_size):
                    chunk = data[i:i + sample_chunk_size]
                    f.write(chunk)
                    progress.update(chunk.shape[0])
        print(f"Saved to {output}.")
    except Exception as e:
        print(f"Unhandled error {e} during audio saving process.")
        return

def ftaud_main(inputp, audioformat, chunksz=16384):
    print(f"Info: Read chunk size <{chunksz}>, Read file <{inputp}>")
    if not os.path.exists(inputp):
        print(f"File {inputp} not found. Is it in your current working directory and accessible?")
        print("Please note that file names are case sensitive.")
        return 1

    if audioformat == "c":
        output = inputp + ".ogg"
    else:
        output = inputp + ".wav"
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

    ftaud_audio(values, output, audioformat)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide an argument.")
        print("Example usage: python3 ftaud.py song.wav c")
        print("Example usage: python3 ftaud.py image.png r")
        sys.exit(1)

    inputp = sys.argv[1]
    audioformat = sys.argv[2]
    ftaud_main(inputp, audioformat)
