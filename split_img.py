from glob import glob
import tifffile
from cellpose.io import imread
import numpy as np
import re

filenames = sorted(glob("/home/jan.woyzichovski/Documents/neurite_test_001/raw/*"))
train_dir = "/home/jan.woyzichovski/Documents/neurite_test_001/train/"
test_dir = "/home/jan.woyzichovski/Documents/neurite_test_001/test/"


for file in filenames:
    img = imread(file)
    h,w = img.shape
    top_img = img[0:h//2, 0:w]
    bot_img = img[h//2:h, 0:w]
    if bool(re.search("_img.tiff", file)):
        tifffile.imwrite(train_dir + re.split("/", file)[-1][0:-9] + "_train_img"  +'.tif', top_img.astype(np.uint16))
        tifffile.imwrite(test_dir + re.split("/", file)[-1][0:-9] + "_test_img"  +'.tif', bot_img.astype(np.uint16))
    else:
        tifffile.imwrite(train_dir + re.split("/", file)[-1][0:-10] + "_train_mask"  +'.tif', top_img.astype(np.uint16))
        tifffile.imwrite(test_dir + re.split("/", file)[-1][0:-10] + "_test_mask"  +'.tif', bot_img.astype(np.uint16))


