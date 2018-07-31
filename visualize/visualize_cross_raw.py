# visualization of mean variance explained cross subject raw
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
main_out_dir = '/Users/chloe/Documents/figure_cross_raw_pc_1/'
### work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_denoise_pca_1_cross/'
### main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/figure_cross_raw_pc_1/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS']
total_run = 8
figure_min = 0
figure_max = 1
title_y = 1.15
labelpad_x = -300

# iterate through all combinations of subjects (including within subject)
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in it.chain(range(0, sub_1_index), range(sub_1_index + 1, len(all_subjects))):
		# initialize info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_raw_ratio_chart.npy'
		out_dir = main_out_dir + sub_1 + '_to_' + sub_2 + '.png'
		if not os.path.exists(main_out_dir):
			os.makedirs(main_out_dir)
		# load data
		data = np.load(data_dir)
		
		# generate figure
		plt.matshow(data, vmin=figure_min, vmax=figure_max) # plot matrix
		plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
		plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
		plt.colorbar() # show color bar
		plt.ylabel('Predictor') # set y axis label
		plt.title(sub_1 + ' to ' + sub_2 + ' mean var explained raw', y=title_y) # set title
		plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
		plt.savefig(out_dir) # save figure
