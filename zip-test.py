from PIL import Image
import getopt, sys, math, os, struct, timeit, zipfile, subprocess
from sys import platform

input_image_path = "pic.png"
input_file_path = "a.txt"
key = "MSW"
k = key.encode('utf-8')
path = os.path.dirname(os.path.abspath(__file__))

image = Image.open(input_image_path)
input_file = open(input_file_path, "rb")

#input_file_path = path + '/' + input_file_path
#print (input_file_path)
#rc = subprocess.call(['7z', 'a', "-p"+key, '-y', 'myzipfile.zip'] + [ input_file_path ])
if platform == "linux" or platform == "linux2":
    # linux
    rc = subprocess.call(['7z', 'a', "-p"+key, '-y', 'myzipfile.zip'] + [ input_file_path ])
elif platform == "darwin":
    # OS X
    rc = subprocess.call(['7z', 'a', "-p"+key, '-y', 'myzipfile.zip'] + [ input_file_path ])
elif platform == "win32":
    # Windows...
    rc = subprocess.call(['7z', 'a', "-p"+key, '-y', 'myzipfile.zip'] + [ input_file_path ], shell=True)
    #rc = subprocess.call(['C:\Program Files\7-Zip\7z.exe', 'a', "-p"+key, '-y', 'myzipfile.zip'] + [ input_file_path ])
#zf = zipfile.ZipFile("myzipfile.zip", "w")
#zf.setpassword(k)
#zf.write(input_file_path)

#zf.extractall(path="extracted")
print("Extracting contents now to folder 'extracted'")
with zipfile.ZipFile("myzipfile.zip", "r") as zf:
    zf.setpassword(k)
    zf.extractall(path="extracted")
