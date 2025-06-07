# fileto
[License](https://sprow.dev/license)
Your (probably not) goto file converter for tough situations.

Currently includes:
 + Any file to PNG
In development:
 + Any file to sound

Requirements:
  Any file to PNG: Pillow and tqdm.

How these work:
 + Reads the file into a list of individual bytes in batches of 16KiB.
 + Gets each byte as a number based on the original binary of the file (Because the list is stored in byte strings which don't have encoding.)
 + Assigns each number to an RGB value. (Byte 1 is R, byte 2 is G, and byte 3 is B and so on.)
 + Writes it to an image using Python's general-use imaging library Pillow.
