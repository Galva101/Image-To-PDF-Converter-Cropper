# All the necessary parameters are accessible after line 55,
# but can of course be changed manually in the Code


# imports for the crop, rename to avoid conflict with reportlab Image import
from PIL import Image as imgPIL
from PIL import ImageChops
import os.path, sys

# import for the PDF creation
import glob
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.platypus import Image, SimpleDocTemplate, Spacer
from reportlab.lib.units import mm, inch

# get os path for Cropping
path = (os.path.dirname(os.path.abspath("cropPDF.py")))
dirs = os.listdir(path)


def trim(im, border="white"):
    bg = imgPIL.new(im.mode, im.size, border)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def crop():
    for item in dirs:
        try:
            fullpath = os.path.join(path, item)
            if os.path.isfile(fullpath):
                im = imgPIL.open(fullpath)
                f, e = os.path.splitext(fullpath)
                imCrop = trim(im, "white")
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

outputName = "output.pdf"

margin = 0.5
imageWidthDefault = 550
spacerHeight = 7
scalingIfImageTooTall = 0.95  # larger than 95 can result in an empty page after the image

includePagenumbers = True
numberFontSize = 10
pageNumberSpacing = 5

############################

if executeCrop:
    crop()

filelist = glob.glob("*.png")  # Get a list of files in the current directory
filelist.sort()

doc = SimpleDocTemplate(
    outputName,
    topMargin=margin * mm,
    leftMargin=margin * mm,
    rightMargin=margin * mm,
    bottomMargin=margin * mm,
    pagesize=A4
)

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
        onLaterPages=add_page_number,
    )
elif not len(filelist) == 0:
    doc.build(story)
else:  # to prevent an empty PDF that can't be opened
    print("no files found")
