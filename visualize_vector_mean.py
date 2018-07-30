# visualize the chart of all subject vector mean value
import os, time
import numpy as np
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_subjects_num = ['01', '02', '04', '05', '09', '15', '16', '17', '18', '19', '20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
out_dir = main_out_dir + 'sub_vector_matrix.png'
figure_max = 0.05
figure_min = 0
title_y = 1.15 # title distance to the top margin
labelpad_x = -300
matrix = np.zeros((len(all_subjects), len(all_subjects))) # initialize overall mean data matrix

# fill in matrix values
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# initialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_vector.npy'
		data = np.load(data_dir)
		mean = data.mean()
		matrix[sub_1_index, sub_2_index] = mean

# generate figure
plt.matshow(matrix, vmin=figure_min, vmax=figure_max, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_subjects)), all_subjects_num) # set x axis tick
plt.yticks(np.arange(len(all_subjects)).T, all_subjects_num) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor subject') # set y axis label
plt.title('mean var explained raw of all regions, pc=3', y=title_y) # set title
plt.xlabel('Target subject', labelpad=labelpad_x) # set x axis label
plt.savefig(out_dir) # save figure

		