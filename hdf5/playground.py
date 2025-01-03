import h5py
import os
import glob
import cv2

import numpy as np

# initializing a random numpy array
arr = np.random.randn(1000)

data_dir = r'images'
hdf5_path = 'test.hdf5'

# creating a file
with h5py.File(hdf5_path, 'w') as f:
    img_grp = f.create_group('images')
    dset = f.create_dataset("default", data=arr)
    # f.close()
    for cnt, ifile in enumerate(glob.iglob(data_dir + '/*.jpg')):
        img = cv2.imread(ifile, cv2.IMREAD_COLOR)
        # or use cv2.IMREAD_GRAYSCALE, cv2.IMREAD_UNCHANGED
        img_ds = img_grp.create_dataset('images_' + f'{cnt + 1:03}', data=img)
    # del f['images']
    #f.close()

