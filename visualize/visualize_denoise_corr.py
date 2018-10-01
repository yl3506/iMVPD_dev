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
out_dir = main_out_dir + 'single_denoise_corr.png'
all_denoise = ['cos', 'compcorr', 'global', 'xyz']
figure_min = 0.955
figure_max = 1
title_y = 1.15

# load var ratio data
data = np.load(work_dir + 'single_denoise_corr.npy')
# remove diagonal
data[range(len(all_denoise)), range(len(all_denoise))] = np.nan

# generate figure
plt.matshow(data, vmin=figure_min, vmax=figure_max, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_denoise)), all_denoise) # set x axis tick
plt.yticks(np.arange(len(all_denoise)).T, all_denoise) # set y axis tick
#plt.xticks.set_fontsize(20)
#plt.rc('xtick',labelsize=20)
plt.tick_params(labelsize=18)
plt.xticks(rotation=30)
#plt.yticks.set_fontsize(20)
#plt.rc('ytick',labelsize=20)
#plt.yticks(rotation=65)
plt.yticks(rotation=60)
plt.colorbar() # show color bar
#plt.title('correlation of single denoising, var ratio, pc=3', y=title_y) # set title
plt.savefig(out_dir) # save figure
