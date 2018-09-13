# visualization of mean variance explained raw (cross-within) subject
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_pc3_v3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'vs_cos_pc3_v3.png'
data_out_dir = work_dir + 'vs_cos_pc3_v3.npy'
#all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
figure_min = 0
figure_max = 0.32
title_y = 1.15
labelpad_x = -300
data_cross = np.zeros((len(all_masks), len(all_masks))) # overall cross data matrix
data_within = np.zeros((len(all_masks), len(all_masks))) # overall within data matrix
data = np.zeros((len(all_masks), len(all_masks))) # data_cross - data_within
count_cross = 0
count_within = 0


# iterate through all combinations of cross subjects 
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in it.chain(range(0, sub_1_index), range(sub_1_index + 1, len(all_subjects))):
		# initialize info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_cross_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_raw_ratio_chart.npy'
		# load data_cross
		data_cross += np.load(data_cross_dir)
		count_cross += 1

# iterate through all within subject
for sub_index in range(0, len(all_subjects)):
	# initialize info
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	data_within_dir = sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy'
	# load data_within
	data_within += np.load(data_within_dir)
	count_within += 1

# calculate mean of all matrices
data_cross = data_cross / count_cross
data_within = data_within / count_within
data = data_within - data_cross
# erase diagonal
data[range(len(all_masks)), range(len(all_masks))] = np.nan
# save data
np.save(data_out_dir, data)

# generate figure
plt.matshow(data, vmin=figure_min, vmax=figure_max, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor') # set y axis label
plt.title('within-cross var raw, cos, pc=3', y=title_y) # set title
plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
plt.savefig(out_dir) # save figure
