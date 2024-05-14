from cellpose import models, io, train
#from cellpose.io import imread
#import numpy as np
from glob import glob
import tifffile


#filenames = sorted(glob("/home/jan.woyzichovski/Documents/neurite_test_001/*.tiff"))
train_dir = "/home/jan.woyzichovski/Documents/neurite_test_001/train/"
test_dir = "/home/jan.woyzichovski/Documents/neurite_test_001/test/"

io.logger_setup()

output = io.load_train_test_data(train_dir, test_dir, image_filter="_img",
                                mask_filter="_masks", look_one_level_down=False)

images, labels, image_names, test_images, test_labels, image_names_test = output

# retrain the Cellpose model cyto
model = models.CellposeModel(model_type="cyto")

model_path = train.train_seg(model.net, train_data=images, train_labels=labels,
                            channels=[1,2], normalize=True, # channels = [0,1]
                            test_data=test_images, test_labels=test_labels,
                            weight_decay=1e-4, SGD=True, learning_rate=0.1,
                            n_epochs=100, model_name="adapt_cyto_01")
