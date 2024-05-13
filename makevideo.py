from pylibCZIrw import czi as pyczi
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from PIL import Image
import matplotlib.cm as cm
import numpy as np

filepath = '/group/dl4miacourse/projects/neurite_trace/#####/Experiment-144.czi'

x_size = 500
y_size = 500
x_tile_num = 4
y_tile_num = 4
tile_margin_x = 139
tile_margin_y = 143
time_channel = 145

scene_of_interest = [9]

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
                    
                    crop_array = center_tile.reshape(6, 256, 4, 256).swapaxes(1, 2) #
                    # crop_0_0 = crop_array[0, 0] #
                    crops = [crop_array[i, j] for i in range(crop_array.shape[0]) for j in range(crop_array.shape[1])] 
                    for count, crop in enumerate(crops):
                        file_name = 'scene_' + scene_id + '_tile_' + x_tile + '_' + y_tile + '_crop_' + count + '_time_' + time_point'.tiff'
                        im = Image.fromarray(np.squeeze(crop, axis=2))
                        im.save("/group/dl4miacourse/projects/neurite_trace/##/" + file_name)
                
 """                for moment in range(145):
                    if x_tile == 0:
                        frame_0 = czidoc.read(plane={"T": moment, "Z": 3, "C": 0}, roi=box)
                        fig, ax = plt.subplots(1, 1, figsize=(15, 15))
                        ax.imshow(frame_0[..., 0], cmap=cm.Grays)
                        plt.show()

                        #im = Image.fromarray(np.squeeze(frame_0, axis=2))
                        #im.save("data/OICE/test.tiff")


                        k = 3

        k = 3

        x_pieces = scene[2] // x_size
        y_pieces = scene[3] // y_size
        x_remainder = scene[2] % x_size
        y_remainder = scene[3] % y_size

        for yy in range(y_pieces + (1 if y_remainder > 0 else 0)):
            for xx in range(x_pieces + (1 if x_remainder > 0 else 0)):
                left = scene[0] + (xx * x_size)
                upper = scene[1] + (yy * y_size)
                right = min(left + x_size, scene[0] + scene[2])
                lower = min(upper + y_size, scene[1] + scene[3])
                box = (left, upper, right-left, lower-upper)

                frame_1 = czidoc.read(plane={"T": 0, "Z": 3, "C": 0}, roi=box)
                fig, ax = plt.subplots(1, 1, figsize=(15, 15))
                ax.imshow(frame_1[..., 0], cmap=cm.Grays)
                plt.show()
                k=3

k = 3 """