# create vector of var explained raw for each subject pair
import os, time
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']

# iterate through all combinations of subjects (including within subject)
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# initialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		out_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_vector.npy'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_raw_ratio_chart.npy'
		data = np.load(data_dir)
		vector = data.reshape(len(all_masks) * len(all_masks), 1) # r x 1
		# save to file
		np.save(out_dir, vector)