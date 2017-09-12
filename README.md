Crypto-steganography of Images
==============================

This tool was developed as a part of my 7th semester projects in Digital Signal Processing.

In this project, we deal with the hiding of data in images.
However, alongside simply hiding the images, we also employ cryptography so that the message cannot be easily recovered by an unauthorized third party.

Initially, I have made a python script which is meant to be run interactively. Further, support for command line arguments will be added to increase ease of use.

The project currently uses an implementation of Vignere cipher. This cipher is ideal only for text files. It becomes possible to generate an output but case and spaces are modified. Another ciphering technique will be needed to allow multiple file formats

Using the virtual environment ->
 ```bash
    pip install virtualenv
    virtualenv virt-env              #Creates a folder of this name which needs to be in .gitignore
    source virt-env/source/activate  #To get into the virtual environment
    deactivate                       #To quit virtual environment
 ```
Using the project on your system ->
 - Install python 3
 - pip install -r requirements.txt

Sample running commands:

    C:\Users\super\Documents\GitHub\crypto-steganography-img>py img-steg.py -h -i pic.png -f a.txt -o steg.png -k MSW -c 1
        Hiding 23 bytes
        Runtime: 1.42 s  
    C:\Users\super\Documents\GitHub\crypto-steganography-img>py img-steg.py -r -i steg.png -o b.txt -k MSW -c 1
        Looking to recover 23 bytes
        Runtime: 0.67 s
