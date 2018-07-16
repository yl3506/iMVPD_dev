# create matrix of correlation ratio
import os, time
import numpy as np

# initialize parameters
work_dir = '/Users/chloe/Documents/'
main_out_dir = '/Users/chloe/Documents/output_denoise_pca_test_pc1/'
all_subjects = ['sub-02', 'sub-03']
### work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
### main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_denoise_normalized/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rATL', 'rFFA', 'rOFA', 'rSTS']
total_run = 8

# iterate through all combinations of subjects (including within subject)
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# iniialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = main_out_dir + sub_1 + '_to_' + sub_2 + '/'
		out_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_ceil_ratio_chart.npy'
		chart = np.zeros((len(all_masks), len(all_masks)))
		# iterate through all combinations of mask
		for mask_1_index in range(0, len(all_masks)):
			for mask_2_index in range(0, len(all_masks)):
				# initialize mask data
				mask_1 = all_masks[mask_1_index]
				mask_2 = all_masks[mask_2_index]
				mask_dir = sub_dir + mask_1 + '_to_' + mask_2 + '/'
				ceil_mean = 0
				# iterate through all runs to calculate mean of ceil_ratio
				for run in range(1, total_run + 1):
					# get ceil_ratio data of current run
					cur_ceil_ratio_dir = mask_dir + 'run_' + str(run) + '_linear_regression_ceil_ratio.txt'
					cur_ceil_ratio = float(np.loadtxt(cur_ceil_ratio_dir))
					# increment ceil_mean
					ceil_mean += cur_ceil_ratio
				# calculate the mean of all runs of current mask pair
				ceil_mean = ceil_mean / total_run
				chart[mask_1_index, mask_2_index] = ceil_mean
		# save current chart to file
		np.save(out_dir, chart)
				