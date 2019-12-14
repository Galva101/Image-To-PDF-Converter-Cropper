This python script takes a folder full of Images, currently specified as PNG,
crops their white border away, and creates a PDF file with those new images.

To run it, python is needed, and Reportlab, which can be done using:
pip install pillow reportlab

Please note, that the images are automatically saved, work with copies if you don't want to edit the originals.
Other file types work as well, if the images are, however not PNG, they will be saved as such while cropping, and then they are used in the PDF.
The image File type can be edited in the .py file, as well as the margins and the scaling inside the PDF.
