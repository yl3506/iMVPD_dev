# visualization of overall mean variance explained within subject as ratio to ceiling
import os
import numpy as np
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3_local/'
### main_out_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3_v3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'overall_within_ceil_pc3_v3.png'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
figure_min = 0
figure_max = 0.3
title_y = 1.15
labelpad_x = -300
data = np.zeros((len(all_masks), len(all_masks))) # initialize overall mean data matrix
count = 0

# iterate through all combinations of subjects (including within subject)
for sub_index in range(0, len(all_subjects)):
	
	# initialize info
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	data_dir = sub_dir + subject + '_to_' + subject + '_ceil_ratio_chart_within.npy'
	if not os.path.exists(main_out_dir):
		os.makedirs(main_out_dir)
	# load data
	data += np.load(data_dir)
	count += 1

# calculate mean of all matrices
data = data / count
# set data diagonal to NaN
data[range(len(all_masks)), range(len(all_masks))] = np.nan
# generate figure
plt.matshow(data, vmin=figure_min, vmax=figure_max, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor') # set y axis label
plt.title('overall within ceil, cos+compcorr, pc=3', y=title_y) # set title
plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
plt.savefig(out_dir) # save figure
