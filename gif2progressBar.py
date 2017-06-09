#!/usr/bin/env python
__author__ = "@ustundag"

import sys, math, numpy
from PIL import Image
import imageio

def processImage(infile):
    try:
        im = Image.open(infile)
    except IOError:
        print("File not found! ", infile)
        sys.exit(1)

    i = 0
    mypalette = im.getpalette()
    frames = []
    try:
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            frames.append(new_im)
            i += 1
            im.seek(im.tell() + 1)
    except EOFError:
        pass # end of frames
    
    return frames

gif_file = sys.argv[1]
frames = processImage(gif_file)
frame_count = len(frames)
im = Image.open(gif_file)
size = im.size
bar_size = math.ceil(size[0]/frame_count)
x_pos = 0
y_pos = size[1] - bar_size
progress_frames = []

i = 0
for im in frames:
    frame_bar = Image.new('RGBA', (bar_size+(bar_size*i), bar_size), (255, 0, 0, 0))
    im.paste(frame_bar, (x_pos, y_pos))
    progress_frames.append(numpy.array(im))
    i += 1

new_filename = 'progressBar_' + sys.argv[1]
imageio.mimwrite(new_filename, progress_frames)
print("GIF with progress bar created, ", new_filename)
