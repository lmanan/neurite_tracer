from cellpose import models, io
from cellpose.io import imread
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.cm as cm
from PIL import Image
from pylibCZIrw import czi as pyczi

# load in data

# convert czi to tiff and crop it


files = ['/group/dl4miacourse/projects/neurite_trace/#####/Experiment-144.czi']



imgs = [imread(f) for f in files]
nimg = len(imgs)

# load model
# model param:
channels = [[0,0]]
cell_diameter = 30 # um 

#model setup:
# test through different models --> cyto, cyto_02, cyto_03
model = models.CellposeModel(model_type="livecell_cp3")

# cell diameter varies !
masks, flows, styles, diams = model.eval(imgs, diameter=cell_diameter, channels=channels)

# eval



# apply the model

