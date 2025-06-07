# fileto
[License](https://sprow.dev/license)\
Your (probably not) goto file converter for tough situations.

Currently includes:
 + Any file to PNG\
 + Any file to sound

Requirements:\
  ftimg: Pillow and tqdm.\
  ftaud: Numpy, tqdm, and soundfile

How these work:
 + Reads the file into a list of individual bytes in batches of 16KiB.
 + Gets each byte as a number based on the original binary of the file (Because the list is stored in byte strings which don't have encoding.)
 + Use a specialized process for each one to turn it into a specific file format (like .wav, .ogg, or .png)
