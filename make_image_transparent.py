import sys
from PIL import Image



def black(img):
    im = Image.open(img)
    newIm = Image.new('RGBA', im.size)
    newIm.save(img)


if len(sys.argv) < 2:
    sys.exit("GIVE FILE PLOX")

for i in range(1, len(sys.argv)):
    black(sys.argv[i])
