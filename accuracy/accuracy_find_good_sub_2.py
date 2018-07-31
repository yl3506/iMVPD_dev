# create matrix of raw variance ratio
import os, time
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']

# iterate through all combinations of subjects (including within subject)
for sub_index in range(0, len(all_subjects)):
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	data_dir = sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy'
	valid_flag = True
	# load raw variance ratio matrix
	matrix = np.load(data_dir)
	temp_matrix = np.zeros(len(all_masks))
	# load the diagonal to temp_matrix
	for i in range(0, len(all_masks)):
		temp_matrix[i] = matrix[i, i]
	# calculate mean and standard deviation
	mean = np.mean(temp_matrix)
	std = np.std(temp_matrix)
	threshold = mean - 2*std
	# iterate through temp_matrix, if lower than mean-2std, then not valid
	for i in range(0, len(temp_matrix)):
		if temp_matrix[i] < threshold:
			valid_flag = False
	# report current subject if valid
	if valid_flag:
		print('valid subject: ' + subject)
