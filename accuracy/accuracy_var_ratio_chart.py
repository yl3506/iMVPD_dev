# calculate the overall raw variance explained for each pair and their var ratio to the matrix mean
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
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

# save overall matrix
overall_out = work_dir + 'overall_raw_var_chart.npy'
np.save(overall_out, data)

# calculate raw ratio and save
data_mean = data.mean()
data_ratio = (data - data_mean) / data_mean

# save ratio matrix
ratio_out = work_dir + 'overall_raw_var_ratio_chart.npy'
np.save(ratio_out, data_ratio)
