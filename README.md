Crypto-steganography of Images
==============================

This tool was developed as a part of my 7th semester projects in Digital Signal Processing.

In this project, we deal with the hiding of data in images.
However, alongside simply hiding the images, we also employ cryptography so that the message cannot be easily recovered by an unauthorized third party.

Initially, I have made a python script which is meant to be run interactively. Further, support for command line arguments will be added to increase ease of use.

The project currently uses an implementation of Vignere cipher. This cipher is ideal only for text files. It becomes possible to generate an output but case and spaces are modified. Another ciphering technique will be needed to allow multiple file formats

Using the project on your system ->
  * Install python 3
  * pip install pycipher
  * pip install Pillow
  * py -i img-steg.py

  Set the following variables, depending on what you want to do.

      # Path of the image to hide data in
  	# Default is "pic.png"
  	input_image_path = "directory\pic.png"

  	# Path of the image to recover data from OR
  	# Path to write steganographed image
  	# Default is "steg_image.png"
  	steg_image_path = "directory\steg_image.png"

  	# Path of file to hide in image
  	# Default is "input.zip"
  	input_file_path = "directory\a.txt"

  	# Path of file to recover data to
  	# Default is "output.zip"
  	output_file_path = "directory\b.txt"

  	# Number of least signifcant bits to use when hiding or recovering data
  	# Default is 2
  	num_lsb = 2

    # Key used for vignere cipher
    # Default is "MihirWagle"
    key = "MihirWagle"

  	# How much to compress image when saving as .png
  	# 1 gives best speed, 9 gives best compression
  	# Default is 1
  	compression = 1
