# visualize correlation of subjects by within-MVPD raw var
import os
import numpy as np
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_global_compcorr_pc3_v3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'corr_sub_within.png'
all_subjects = ['01', '02', '04', '05', '09', '15', '16', '17', '18', '19', '20']
figure_min = 0.9
figure_max = 1
title_y = 1.15

# load var ratio data
data = np.load(work_dir + 'corr_sub_within.npy')

# generate figure
plt.matshow(data, vmin=figure_min, vmax=figure_max, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_subjects)), all_subjects) # set x axis tick
plt.yticks(np.arange(len(all_subjects)).T, all_subjects) # set y axis tick
plt.colorbar() # show color bar
plt.title('subjects corr (within-MVPD raw var), glb+cpcr, pc=3', y=title_y) # set title
plt.savefig(out_dir) # save figure
