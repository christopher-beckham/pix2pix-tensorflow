"""
Create an HDF5 version of the Google Maps atob dataset
for pix2pix applications.
"""

import sys
import os
import glob
from skimage.io import imread, imsave
import h5py

train_files = glob.glob("maps/train/*.jpg")
valid_files = glob.glob("maps/val/*.jpg")

f = h5py.File("maps/maps.h5", "w")
f.create_dataset('xt', shape=(len(train_files), 512, 512, 3), dtype='uint8')
f.create_dataset('yt', shape=(len(train_files), 512, 512, 3), dtype='uint8')
f.create_dataset('xv', shape=(len(valid_files), 512, 512, 3), dtype='uint8')
f.create_dataset('yv', shape=(len(valid_files), 512, 512, 3), dtype='uint8')

print "len train files:", len(train_files)
print "len valid files:", len(valid_files)

def get_a_b(img):
    # cut image in half
    a,b = img[:,0:600,:], img[:,600::,:]
    # go from 600px to 512px
    a, b = a[0:512,0:512,:], b[0:512,0:512,:]
    return a,b

for idx, filename in enumerate(train_files):
    img = imread(filename)
    a,b = get_a_b(img)
    f['xt'][idx] = a
    f['yt'][idx] = b
    
for idx, filename in enumerate(valid_files):
    img = imread(filename)
    a,b = get_a_b(img)
    f['xv'][idx] = a
    f['yv'][idx] = b
    
f.close()
