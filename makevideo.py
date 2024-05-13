from pylibCZIrw import czi as pyczi
from scipy.ndimage import zoom
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from PIL import Image
import matplotlib.cm as cm
import numpy as np

project_path = '/Volumes/T7 Shield/20240503/'
filepath = '/Volumes/T7 Shield/20240503/Experiment-144.czi'

x_size = 500
y_size = 500
x_tile_num = 4
y_tile_num = 4
tile_margin_x = 139
tile_margin_y = 143
time_channel = 145

scene_of_interest = [0]

with pyczi.open_czi(filepath) as czidoc:

    scenes_bounding = czidoc.scenes_bounding_rectangle
    pixel_type = czidoc.get_channel_pixel_type(0)

    for scene_id in scene_of_interest:
        scene = scenes_bounding[scene_id]

        x_width = scene[2] // x_tile_num #  tiles width
        y_width = scene[3] // y_tile_num #  tiles height

        for y_tile in range(y_tile_num):
            for x_tile in range(x_tile_num):
                left = scene[0] + (x_tile * x_width)
                upper = scene[1] + (y_tile * y_width)
                box = (left + tile_margin_x, upper + tile_margin_y, x_width - tile_margin_x * 2, y_width - tile_margin_y * 2)
                for time_point in range(time_channel):
                    center_tile = czidoc.read(plane={"T": time_point, "Z": 3, "C": 0}, roi=box)
                    print(center_tile.shape) 
                    
                    #crop_array = center_tile.reshape(4, 256, 6, 256).swapaxes(1, 2)
                    crop_array = center_tile.reshape(2, 512, 3, 512).swapaxes(1, 2)#
                    # crop_0_0 = crop_array[0, 0] #
                    crops = [crop_array[i, j] for i in range(crop_array.shape[0]) for j in range(crop_array.shape[1])] 
                    for count, crop in enumerate(crops):
                        file_name = 'scene_' + str(scene_id) + '_tile_' + str(x_tile) + '_' + str(y_tile) + '_crop_' + str(count) + '_time_' + str(time_point) + '.tiff'
                        #im = Image.fromarray(crop)
                        #im.save(project_path + 'pics/256_256_original/' + file_name)
                        #for 512
                        zoom_factor = [n / o for n, o in zip((256,256), crop.shape)]
                        resized_crop = zoom(crop, zoom_factor, order=3)  # 'order=3' for bicubic interpolation
                        im = Image.fromarray(resized_crop)
                        im.save(project_path + 'pics/256_256_from_512_512/' + file_name)

                        k = 3
