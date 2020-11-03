# All the necessary parameters are accessible after line 116,
# but can of course be changed manually in the Code
# reportlab is also needed, to install run: pip install pillow reportlab


# imports for the crop, rename to avoid conflict with reportlab Image import
from PIL import Image as imgPIL
from PIL import ImageChops, ImageOps, ImageFilter
import os.path, sys

# import for the PDF creation
import glob
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm, mm
from reportlab.lib import utils
from reportlab.platypus import Image, SimpleDocTemplate, Spacer
from reportlab.pdfgen import canvas

# PyPDF2 for the metadata modification
from PyPDF2 import PdfFileReader, PdfFileWriter

# get os path for Cropping
path = (os.path.dirname(os.path.abspath("cropPDF.py")))
dirs = os.listdir(path)


def trim(im, border="grey"):
    bg = imgPIL.new(im.mode, im.size, border)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def findMaxWidth():
    maxWidth = 0
    for item in dirs:
        try:
            fullpath = os.path.join(path, item)
            if os.path.isfile(fullpath):
                im = imgPIL.open(fullpath)
                maxWidth = max(maxWidth, im.size[0])
        except:
            pass
    return maxWidth


def padImages(docHeight):
    path = (os.path.dirname(os.path.abspath("cropPDF.py"))) #redundancy in case any images change
    dirs = os.listdir(path)
    maxWidth = findMaxWidth()
    for item in dirs:
        try:
            fullpath = os.path.join(path, item)
            if os.path.isfile(fullpath):
                im = imgPIL.open(fullpath)
                f, e = os.path.splitext(fullpath)

                width, height = im.size  # get the image dimensions, the height is needed for the blank image
                if not docHeight <= height:  # to prevent oversized images from bein padded, such that they remain centered
                    image = imgPIL.new('RGB', (maxWidth, height),
                                       (255, 255, 255))  # create a white image with the max width			
                    image.paste(im, (0, 0))  # paste the original image overtop the blank one, flush on the left side
                    image.save(f + ".png", "PNG", quality=100)
        except:
            pass
            
            
def addSeparators( separatorHeight ):
    if separatorHeight <1:
        separatorHeight = 1 #less than one wont be rendered in a PDF reader
    maxWidth = findMaxWidth()
    for item in dirs:
        try:
            fullpath = os.path.join(path, item)
            if os.path.isfile(fullpath):
                im = imgPIL.open(fullpath)
                f, e = os.path.splitext(fullpath)
                width, height = im.size  
                height = height + separatorHeight
                image = imgPIL.new('RGB', (maxWidth, height),(0, 0, 0))  		
                image.paste(im, (0, 0))  
                image.save(f + ".png", "PNG", quality=100)
        except:
            pass


def crop():
    path = (os.path.dirname(os.path.abspath("cropPDF.py"))) #redundancy in case any images change
    dirs = os.listdir(path)
    for item in dirs:
        for colour in ["black", "white", "grey", "yellow", "orange", "amber"]:
            try:            
                fullpath = os.path.join(path, item)
                if os.path.isfile(fullpath):
                    im = imgPIL.open(fullpath)
                    f, e = os.path.splitext(fullpath)
                    imCrop = trim(im, colour)
                    imCrop.save(f + ".png", "PNG", quality=100)
            except:
                pass


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', numberFontSize)
    page_number_text = "%d" % (doc.page)
    canvas.drawCentredString(
        pageNumberSpacing * mm,
        pageNumberSpacing * mm,
        page_number_text
    )
    canvas.restoreState()


#############################

executeCrop = True
executePad = True
includeSeparators = True

outputName = "output.pdf"  # The name of the file that will be created

margin = 0.5
imageWidthDefault = 550
spacerHeight = 7
scalingIfImageTooTall = 0.95  # larger than 95 can result in an empty page after the image
separatorHeight = 1

includePagenumbers = True
numberFontSize = 10
pageNumberSpacing = 5

author = "Galva101"
title = "CropPDF"
subject = "GitHub"

############################
doc = SimpleDocTemplate(
    outputName,
    topMargin=margin * mm,
    leftMargin=margin * mm,
    rightMargin=margin * mm,
    bottomMargin=margin * mm,
    pagesize=A4
)

if executeCrop:
    crop()
if executePad:
    padImages(doc.height)
if includeSeparators:
    addSeparators(separatorHeight)

filelist = glob.glob("*.png")  # Get a list of files in the current directory
filelist.sort()

story = []  # create the list of images for the PDF

for fn in filelist:
    img = utils.ImageReader(fn)
    img_width, img_height = img.getSize()  # necessary for the aspect ratio
    aspect = img_height / float(img_width)

    documentHeight = doc.height

    imageWidth = imageWidthDefault
    imageHeight = imageWidth * aspect	

    if imageHeight > documentHeight:
        imageHeight = documentHeight * scalingIfImageTooTall
        imageWidth = imageHeight / aspect

    img = Image(
        fn,
        width=imageWidth,
        height=imageHeight
    )
    story.append(img)
    space = Spacer(width=0, height=spacerHeight)
    story.append(space)

if includePagenumbers and not len(filelist) == 0:  # if pagenumbers are desired, or not
    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )
elif not len(filelist) == 0:
    doc.build(story)
else:  # to prevent an empty PDF that can't be opened
    print("no files found")

#attemp the metadata edit   
try:
    file = open('output.pdf', 'rb+')
    reader = PdfFileReader(file)
    writer = PdfFileWriter()

    writer.appendPagesFromReader(reader)
    metadata = reader.getDocumentInfo()
    writer.addMetadata(metadata)

    writer.addMetadata({
        '/Author': author,
        '/Title': title,
        '/Subject' : subject,
        '/Producer' : "CropPDF",
        '/Creator' : "CropPDF",
    })
    writer.write(file)
    file.close()
except:
    print("Error while editing metadata")
