"""
FrameConvert, by Philip Stephenson
Used to convert images from framepicture plugin back to normal .png files
Instructions: place frameconvert.py in plugin directory, and run once. Images will output to FrameConvert folder.
Requires Pillow
"""
import os
import re
from PIL import Image

def deleteImg(frame):
    file = os.path.join('FrameConvert', 'Frame' + frame + '.png')
    if os.path.isfile(file):
        os.remove(file)

def joinImg(frame, x, y, alt=0):
    pattern = "Frame%i_%i-%i.png"
    altPattern = "Frame%i_%i-%i_%i.png"
    img = Image.new("RGB", (size * x, size * y))

    for i in range(x):
        for j in range(y):
            if alt == 0:
                file = os.path.join(workdir, pattern % (frame, i, j))
            else:
                file = os.path.join(workdir, altPattern % (frame, i, j, alt))
            if os.path.isfile(file):
                im = Image.open(file)
            else:
                diff = (x - i - 1) + x * (y - j - 1)
                file = os.path.join(workdir, pattern % (frame - diff, i, j))
                if os.path.isfile(file):
                    deleteImg(str(frame - diff))
                    im = Image.open(file)
            try:
                img.paste(im, (i * size, j * size))
            except:
                return
    return img

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

size = 128
workdir = "FramePicture/images"
files = sorted(os.listdir(workdir), key=numericalSort)
last = int(re.search('\d+', files[files.__len__() - 1]).group(0))

if not os.path.isdir('FrameConvert'):
    os.mkdir('FrameConvert')

for i in range(last + 1):
    imgFiles = [x for x in files if (re.search('Frame' + str(i) + '_\d+-\d+', x) and not re.search('Frame' + str(i) + '_\d+-\d+_\d+', x))]
    if imgFiles:
        altFiles = [x for x in files if (re.search('Frame' + str(i) + '_\d+-\d+_\d+', x))]
        if altFiles:
            alts = max([int(re.search('Frame\d+_(\d+)-(\d+)_(\d+)', x).group(3)) for x in altFiles])
            for j in range(1, alts + 1):
                width = max([int(re.search('Frame\d+_(\d+)-(\d+)_' + str(j), x).group(1)) for x in altFiles if re.search('Frame' + str(i) + '_\d+-\d+_' + str(j), x)]) + 1
                height = max([int(re.search('Frame\d+_(\d+)-(\d+)_'+ str(j), x).group(2)) for x in altFiles if re.search('Frame' + str(i) + '_\d+-\d+_' + str(j), x)]) + 1
                image = joinImg(i, width, height, j)
                if image:
                    image.save(os.path.join('FrameConvert', 'Frame' + str(i) + '_' + str(j) + '.png'))

        width = max([int(re.search('Frame\d+_(\d+)-(\d+)', x).group(1)) for x in imgFiles]) + 1
        height = max([int(re.search('Frame\d+_(\d+)-(\d+)', x).group(2)) for x in imgFiles]) + 1
        image = joinImg(i, width, height)
        if image:
            image.save(os.path.join('FrameConvert', 'Frame' + str(i) + '.png'))