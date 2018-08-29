# calculate the overall raw variance explained for each pair and their var ratio to the matrix mean
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
data = np.zeros((len(all_masks), len(all_masks))) # initialize overall mean data matrix
count = 0

# save overall raw var matrix by iterating through all combinations of subjects
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in it.chain(range(0, sub_1_index), range(sub_1_index + 1, len(all_subjects))):
		# initialize info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_raw_ratio_chart.npy'
		# load data
		data += np.load(data_dir)
		count += 1

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
