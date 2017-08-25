# The MIT License (MIT)
#
# Copyright (c) 2017 Mihir Wagle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PIL import Image
from pycipher import Vigenere
import getopt, sys, math, os, struct, timeit

# Number of least significant bits containing/to contain data in image
num_lsb = 2

def prepare_hide():
    # Prepare files for reading and writing for hiding data.
    global image, input_file

    try:
        image = Image.open(input_image_path)
        input_file = open(input_file_path, "rb")
        #print (input_file.read())
    except FileNotFoundError:
        print("Input image or file not found, will not be able to hide data.")

def prepare_recover():
    # Prepare files for reading and writing for recovering data.
    global steg_image, output_file

    try:
        steg_image = Image.open(steg_image_path)
        output_file = open(output_file_path, "wb+")
    except FileNotFoundError:
        print("Steg image not found, will not be able to recover data.")

def reset_buffer():
    global buffer, buffer_length

    buffer = 0
    buffer_length = 0

def and_mask(index, n):
    # Returns an int used to set n bits to 0 from the index:th bit when using
    # bitwise AND on an integer of 8 bits or less.
    # Ex: and_mask(3,2) --> 0b11100111 = 231.
    return 255 - ((1 << n) - 1 << index)

def get_filesize(path):
    # Returns the filesize in bytes of the file at path
    return os.stat(path).st_size

def max_bits_to_hide(image):
    # Returns the number of bits we're able to hide in the image
    # using num_lsb least significant bits.
    # 3 color channels per pixel, num_lsb bits per color channel.
    return int(3 * image.size[0] * image.size[1] * num_lsb)

def bits_in_max_filesize(image):
    # Returns the number of bits needed to store the size of the file.
    return max_bits_to_hide(image).bit_length()

def read_bits_from_buffer(n):
    # Removes the first n bits from the buffer and returns them.
    global buffer, buffer_length

    bits = buffer % (1 << n)
    buffer >>= n
    buffer_length -= n
    return bits

def hide_data():
    # Hides the data from the input file in the input image.
    global buffer, buffer_length, image

    start = timeit.default_timer()
    prepare_hide()
    reset_buffer()
    data1 = input_file.read()
    #print (data1)
    data1 = data1.decode('utf-8')
    ciphered = Vigenere(key).encipher(data1)
    ciphered = ciphered.encode('utf-8')
    data = iter(memoryview(ciphered))

    color_data = list(image.getdata())
    color_data_index = 0

    # We add the size of the input file to the beginning of the buffer.
    buffer += get_filesize(input_file_path)
    buffer_length += bits_in_max_filesize(image)

    print("Hiding", buffer, "bytes")

    if (buffer * 8 + buffer_length > max_bits_to_hide(image)):
        print("Only able to hide", max_bits_to_hide(image) // 8,
              "B in image. PROCESS WILL FAIL!")
    mask = and_mask(0, num_lsb)

    done = False
    while (not done):
        rgb = list(color_data[color_data_index])
        for i in range(3):
            if(buffer_length < num_lsb):
                # If we need more data in the buffer, add a byte from the file to it.
                try:
                    buffer += next(data) << buffer_length
                    buffer_length += 8
                except StopIteration:
                    # If we've reached the end of our data, we're done
                    done = True
            # Replace the num_lsb least significant bits of each color
            # channel with the first num_lsb bits from the buffer.
            rgb[i] &= mask
            rgb[i] |= read_bits_from_buffer(num_lsb)
        color_data[color_data_index] = tuple(rgb)
        color_data_index += 1

    image.putdata(color_data)
    image.save(steg_image_path, compress_level=compression)
    stop = timeit.default_timer()
    print("Runtime: {0:.2f} s".format(stop - start))

def recover_data():
    # Writes the data from the steganographed image to the output file
    global buffer, buffer_length, steg_image

    start = timeit.default_timer()
    prepare_recover()
    reset_buffer()

    data = bytearray()

    color_data = list(steg_image.getdata())
    color_data_index = 0

    pixels_used_for_filesize = math.ceil(bits_in_max_filesize(steg_image)
                                         / (3 * num_lsb))
    for i in range(pixels_used_for_filesize):
        rgb = list(color_data[color_data_index])
        color_data_index += 1
        for i in range(3):
            # Add the num_lsb least significant bits
            # of each color channel to the buffer.
            buffer += (rgb[i] % (1 << num_lsb) << buffer_length)
            buffer_length += num_lsb

    # Get the size of the file we need to recover.
    bytes_to_recover = read_bits_from_buffer(bits_in_max_filesize(steg_image))
    print("Looking to recover", bytes_to_recover, "bytes")

    while (bytes_to_recover > 0):
        rgb = list(color_data[color_data_index])
        color_data_index += 1
        for i in range(3):
            # Add the num_lsb least significant bits
            # of each color channel to the buffer.
            buffer += (rgb[i] % (1 << num_lsb)) << buffer_length
            buffer_length += num_lsb

        while (buffer_length >= 8 and bytes_to_recover > 0):
            # If we have more than a byte in the buffer, add it to data
            # and decrement the number of bytes left to recover.
            bits = read_bits_from_buffer(8)
            data += struct.pack('1B', bits)
            bytes_to_recover -= 1
    data = bytes(data).decode('utf-8')
    decrypted = Vigenere(key).decipher(data)
    decrypted = decrypted.encode('utf-8')
    output_file.write(decrypted)
    output_file.close()

    stop = timeit.default_timer()
    print("Runtime: {0:.2f} s".format(stop - start))

def analysis():
    # Find how much data we can hide and the size of the data to be hidden
    prepare_hide()
    print("Image resolution: (", image.size[0], ",", image.size[1], ")")
    print("Using", num_lsb, "LSBs: we can hide\t",
          max_bits_to_hide(image) // 8, "B")
    print("Size of input file: \t\t", get_filesize(input_file_path), "B")
    print("Filesize tag: \t\t\t",
          math.ceil(bits_in_max_filesize(image) / 8), "B")

def usage():
    print("\nCommand Line Arguments:\n",
          "-h, --hide              To hide data in a sound file\n",
          "-r, --recover           To recover data from a sound file\n",
          "-i, --image=            Path to a .png file\n",
          "-f, --file=             Path to a txt file to hide in the sound file\n",
          "-o, --output=           Path to an output file\n",
          "-k, --key=              How many LSBs to use\n",
          "-c, --compression=      How many bytes to recover from the sound file\n",
          "--help                  Display this message\n")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hri:f:o:k:c:',
                              ['hide', 'recover', 'image=', 'file=',
                               'output=', 'key=', 'compression=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(1)

hiding_data = False
recovering_data = False

for opt, arg in opts:
    if opt in ("-h", "--hide"):
        hiding_data = True
    elif opt in ("-r", "--recover"):
        recovering_data = True
    elif opt in ("-i", "--image"):
        input_image_path = arg
    elif opt in ("-f", "--file"):
        input_file_path = arg
    elif opt in ("-o", "--output"):
        output_file_path = arg
    elif opt in ("-k", "--key="):
        key = arg
    elif opt in ("-c", "--compression="):
        compression = int(arg)
    elif opt in ("--help"):
        usage()
        sys.exit(1)
    else:
        print("Invalid argument {}".format(opt))

try:
    if (hiding_data):
        input_image_path = input_image_path
        input_file_path = input_file_path
        steg_image_path = output_file_path
        key = key
        compression = compression
        hide_data()
    if (recovering_data):
        steg_image_path = input_image_path
        output_file_path = output_file_path
        key = key
        compression = compression
        recover_data()
except Exception as e:
    print("Ran into an error during execution. Check input and try again.\n")
    print(e)
    usage()
    sys.exit(1)
# Initial paths, variables used.
#input_image_path = "pic.png"
#steg_image_path = "steg_image.png"
#input_file_path = "a.txt"
#output_file_path = "b.txt"
#key = "MihirWagle"
#compression = 1
