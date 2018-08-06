# create matrix of raw correlation ratio
import os, time, math
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc1/'
### all_subjects = ['sub-02', 'sub-04']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8

# iterate through all combinations of subjects (including within subject)
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# initialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		# iterate through all combinations of mask
		for mask_1_index in range(0, len(all_masks)):
			for mask_2_index in range(0, len(all_masks)):
				# initialize mask data
				mask_1 = all_masks[mask_1_index]
				mask_2 = all_masks[mask_2_index]
				mask_dir = sub_dir + mask_1 + '_to_' + mask_2 + '/'
				raw_mean = 0
				# iterate through all runs to calculate correlation ratio (sqrt of var raw)
				for run in range(1, total_run + 1):
					# get raw_ratio data of current run
					cur_raw_ratio_dir = mask_dir + 'run_' + str(run) + '_linear_regression_ratio_pc3.txt'
					cur_raw_ratio = float(np.loadtxt(cur_raw_ratio_dir))
					# take sqrt of current ratio
					cur_corr = 0
					if cur_raw_ratio >= 0:
						cur_corr = math.sqrt(cur_raw_ratio)
					# save current correlation to file
					out_dir = mask_dir + 'run_' + str(run) + '_linear_regression_corr_pc3.txt'
					f = open(out_dir, 'w+')
					f.write(str(cur_corr))
					f.close()
				