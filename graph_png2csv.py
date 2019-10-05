from PIL import Image
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd

##open image

org = Image.open('graficimg.png')
im = org.crop((0, 0, 574, 380))

## attempt to get the maximum value, not functional at the moment

# max_value = org.crop((575, 5, 600, 25))
# max_value.save('max.png')

##


im = im.convert('RGBA')
data = np.array(im)
# just use the rgb values for comparison
rgb = data[:,:,:3]
color = [0, 51, 102]   # Original value
black = [0,0,0, 255]
white = [255,255,255,255]
mask = np.all(rgb == color, axis = -1)
# change all pixels that match color to white
data[mask] = black


#crop image to needed size
new_im = Image.fromarray(data)
new_im.save('cropped_file.png')

im = Image.open('cropped_file.png')
R, G, B = im.convert('RGB').split()
r = R.load()
g = G.load()
b = B.load()
w, h = im.size

# Convert non-black pixels to white (only the graph shape)
for i in range(w):
    for j in range(h):
        if(r[i, j] != 0 or g[i, j] != 0 or b[i, j] != 0):
            r[i, j] = 255 # Just change R channel

# Merge just the R channel as all channels
im = Image.merge('RGB', (R, R, R))
im.save("black_and_white.png")

## get the coordinates for every pixel

img_file = Image.open('black_and_white.png')

width, height = img_file.size
format = img_file.format
mode = img_file.mode


img = Image.open("black_and_white.png")
size = w , h = img.size
data = img.load()

pieces = []

for x in range(w):
    for y in range(h):
        hex_color = '#'+ ''.join([hex(it)[2:].zfill(2).upper() for it in data[x,y]])
        #print(hex_color)
        pieces.append((x,y, hex_color))
        #hex_color = '#' + ''.join([hex(it)])

#print(pieces)

## keep only th nonwhite pixels.

sorted = []
for piece in pieces:
    if piece[2] !='#FFFFFF':
        sorted.append(piece)

#print(sorted)

## export a .txt with the coordinates of each pixel from the picture
with open('coords.txt','w') as handle:
    for piece in sorted:
        handle.write(str(piece))

x = []
y = []
z = []
for piece in sorted:
    x.append(piece[0])
    y.append(piece[1])
max = max(y)
#print(max)
for valY in y:
    z.append(max - int(valY)) ## flip the chard right side up
date = np.arange(1, 366, 365 / len(z)) ## convert the X coordinate value to day value
#print(date)

## Create and save the .csv file with the graph values
#print(x)
#print(z)
data = list(zip(date, z))
dataf = pd.DataFrame(data)
for item in dataf:
    dataf.to_csv('data_export.csv', sep=',')
#print(data)
#print(dataf)
# plt.plot(x, z)
# plt.plot(date, z)
# plt.show()