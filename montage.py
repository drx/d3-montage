#!/usr/bin/env python
import os
import sys
from time import strftime
import Image
import ImageDraw
import ImageFont

# parameters
row_size = 4
margin = 5

def generate_montage(filenames):
    images = [Image.open(filename) for filename in filenames]

    width = 0
    height = 0
    i = 0
    sum_x = max_y = 0 
    width = max(image.size[1]+margin for image in images)*row_size
    height = sum(image.size[0]+margin for image in images)

    montage = Image.new(mode='RGBA', size=(width, height), color=(0,0,0,0))
    try:
        image_font = ImageFont.truetype('font/Helvetica.ttf', 18)
    except:
        try:
            image_font = ImageFont.load('font/Helvetica-18.pil')
        except:
            image_font = ImageFont.load_default()
    draw = ImageDraw.Draw(montage)
    offset_x = offset_y = 0

    i = 0
    max_y = 0
    max_x = 0
    offset_x = 0
    for image in images:
        montage.paste(image, (offset_x, offset_y))

        text_coords = offset_x + image.size[0] - 45, offset_y + 120
        draw.text(text_coords, '#{0}'.format(i+1), font=image_font)
        
        max_x = max(max_x, offset_x+image.size[0])
        if i % row_size == row_size-1: 
            offset_y += max_y+margin
            max_y = 0
            offset_x = 0
        else:
            offset_x += image.size[0]+margin
            max_y = max(max_y, image.size[1])

        i += 1

    if i % row_size:
        offset_y += max_y

    filename = strftime("Montage %Y-%m-%d at %H.%M.%S.png")
    montage = montage.crop((0, 0, max_x, offset_y))
    montage.save(filename)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_montage(sys.argv[1:])
