## Description
This python script takes a folder full of Images, currently specified as *PNG*, crops their border away, and creates a PDF file with those new images.

The crop first removes black and white, then it automatically reads the corner of the image, crops those colours, and then some more pre-specified colours.
The images are formatted to be as wide as the PDF page, and one image above the other.
The files are sorted lexicographically before being added to the PDF.

Additional features include the ability to add a frame to each image, add a separator after each image, or even to completely change the colour of the PDF if desired.

## Instructions
To run it, python is needed, as well as Reportlab and PyPDF2 for the renaming of the metadata, which can be installed using:
```
pip install pillow reportlab PyPDF2
```
To run it, execute:
```
python cropPDF.py
```
Please note, that the images are automatically saved, work with copies if you don't want to edit the originals.
Other file types work as well, if the images are, however not *PNG*, they will be saved as such while cropping, and then they are used in the PDF. So far this script has been tested with *PNG, JPG and BMP*.
The image File type can be edited in the *.py* file, as well as the margins and the scaling inside the PDF.
