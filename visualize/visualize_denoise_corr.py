# visualize correlation of single denoising methods performnace
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'single_denoise_corr_matrix.png'
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
figure_min = -1
figure_max = 1
title_y = 1.15
labelpad_x = -300

# load var ratio data
data = np.load(work_dir + 'single_denoise_corr_matrix.npy')

# generate figure
plt.matshow(data, vmin=figure_min, vmax=figure_max) # plot matrix
plt.xticks([0, 7, 14, 21, 28, 35, 42]) # set x axis tick
plt.yticks([0, 7, 14, 21, 28, 35, 42]) # set y axis tick
plt.colorbar() # show color bar
# plt.ylabel('Predictor') # set y axis label
plt.title('single denoising methods correlation, pc=3', y=title_y) # set title
# plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
plt.savefig(out_dir) # save figure
