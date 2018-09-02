# visualize variance ratio for each denoising method performance
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_pc3_v3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'var_ratio_cos.png'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
figure_min = -1.5
figure_max = 3.5
title_y = 1.15
labelpad_x = -300
data = np.zeros((len(all_masks), len(all_masks))) # initialize overall mean data matrix
count = 0

# load var ratio data
data = np.load(work_dir + 'overall_raw_var_ratio_chart.npy')

# generate figure
plt.matshow(data, vmin=figure_min, vmax=figure_max) # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor') # set y axis label
plt.title('var ratio, cos, pc=3', y=title_y) # set title
plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
plt.savefig(out_dir) # save figure
