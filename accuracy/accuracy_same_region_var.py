# within region overall variance expalined raw within and cross
import os, time
import numpy as np
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-04']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_global_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8

# iterate through all masks
for mask_index in range(0, len(all_masks)):
	# initialize mask data
	mask = all_masks[mask_index]
	within_out_dir = work_dir + mask + '_overall_var_within.txt'
	cross_out_dir = work_dir + mask + '_overall_var_cross.txt'
	within_var = 0
	cross_var = 0
	within_num = 0
	cross_num = 0
	
	# consider within subject performance
	for sub_1_index in range(0, len(all_subjects)):
		for sub_2_index in range(0, len(all_subjects)):
			# iniialize data info
			sub_1 = all_subjects[sub_1_index]
			sub_2 = all_subjects[sub_2_index]
			sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
			data_dir = sub_dir + mask + '_to_' + mask + '/'

			if sub_1_index == sub_2_index: # within subject
				var_temp = 0
				within_num += 1
				# iterate thorugh all runs 
				for run in range(1, total_run + 1):
					var_dir = data_dir + 'run_' + str(run) + '_linear_regression_ratio_pc3.txt'
					var_data = float(np.loadtxt(var_dir))
					var_temp += var_data
				var_temp = var_temp / total_run
				within_var += var_temp
			else: # cross subject
				var_temp = 0
				cross_num += 1
				# iterate through all runs
				for run in range(1, total_run + 1):
					var_dir = data_dir + 'run_' + str(run) + '_linear_regression_ratio_pc3.txt'
					var_data = float(np.loadtxt(var_dir))
					var_temp += var_data
				var_temp = var_temp / total_run
				cross_var += var_temp

	# get average performance for current region
	within_var = within_var / within_num
	cross_var = cross_var / cross_num
	# save roi average var to file
	with open(within_out_dir, 'w+') as outfile:
		outfile.write(str(within_var))
	with open(cross_out_dir, 'w+') as outfile:
		outfile.write(str(cross_var))
