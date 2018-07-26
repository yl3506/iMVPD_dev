# report the valid subjects without much noise
import os, time
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_within/'
### all_subjects = ['sub-02', 'sub-05']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
mask = 'rFFA'
total_run = 8
threshold = 0.15 # above the threshold data viewed as valid

# iterate through all subjects
for sub_index in range(0, len(all_subjects)):
	# data initialize	
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	mask_dir = sub_dir + mask + '_to_' + mask + '/'
	valid_flag = True
	# iterate through all runs in this mask pair
	for run in range(1, total_run + 1):
		# load ratio data
		data_dir = mask_dir + 'run_' + str(run) + '_linear_regression_ratio.txt'
		data = float(np.loadtxt(data_dir))
		# data invalid if ever lower than threshold
		if data < threshold:
			valid_flag = False
	# report this subject if valid
	if valid_flag:
		print('valid subject: ' + subject)