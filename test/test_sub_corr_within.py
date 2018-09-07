# calculate correlation of each region prediction for within subject
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_global_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8


# save overall raw var matrix by iterating through all combinations of subjects
for sub_1_index in range(0, len(all_subjects)):
	flat = np.zeros((len(all_masks) * len(all_masks), 2))
	sub_1 = all_subjects[sub_1_index]
	sub_1_dir = work_dir + sub_1 + '_to_' + sub_1 + '/'
	data_1_dir = sub_1_dir + sub_1 + '_to_' + sub_1 + '_raw_ratio_chart.npy'
	data_1 = np.load(data_1_dir)
	flat[:, 0] = np.squeeze(data_1.reshape((len(all_masks) * len(all_masks), -1)))
	for sub_2_index in it.chain(range(0, sub_1_index), range(sub_1_index + 1, len(all_subjects))):
		sub_2 = all_subjects[sub_2_index]
		sub_2_dir = work_dir + sub_2 + '_to_' + sub_2 + '/'
		data_2_dir = sub_2_dir + sub_2 + '_to_' + sub_2 + '_raw_ratio_chart.npy'
		data_2 = np.load(data_2_dir)
		flat[:, 1] = np.squeeze(data_2.reshape((len(all_masks) * len(all_masks), -1)))
		cov = np.cov(flat)


# calculate mean of all matrices
data = data / coun
# save overall matrix
overall_out = work_dir + 'overall_raw_var_chart.npy'
np.save(overall_out, data)

# calculate raw ratio and save
data_mean = data.mean()
data_ratio = (data - data_mean) / data_mean
# save ratio matrix
ratio_out = work_dir + 'overall_raw_var_ratio_chart.npy'
np.save(ratio_out, data_ratio)
