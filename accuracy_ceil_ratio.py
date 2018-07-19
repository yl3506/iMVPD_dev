# calculate ceiling ratio
import os, time, json
import numpy as np
from sklearn import linear_model
import itertools as it
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### main_out_dir = '/Users/chloe/Documents/output_denoise_pca_test_pc1_0205/'
### all_subjects = ['sub-02', 'sub-05']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_denoise_pca_1_cross/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS']
total_run = 8

# iterate through all combinations of subjects (including within subject)
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# iniialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = main_out_dir + sub_1 + '_to_' + sub_2 + '/'
		# iterate through all combinations of mask
		for mask_1_index in range(0, len(all_masks)):
			for mask_2_index in range(0, len(all_masks)):
				# initialize mask data
				mask_1 = all_masks[mask_1_index]
				mask_2 = all_masks[mask_2_index]
				mask_dir = sub_dir + mask_1 + '_to_' + mask_2 + '/'
				# iterate through each run
				for run in range(1, total_run + 1):
					# get ceil var ratio, cross subject but within region
					ceil_dir = sub_dir + mask_2 +'_to_' + mask_2 + '/run_' + str(run) + '_linear_regression_ratio.txt'
					ceil = float(np.loadtxt(ceil_dir))
					# output directory
					out_dir = mask_dir + 'run_' + str(run) + '_linear_regression_ceil_ratio.txt'
					# get variance ratio of current run cross subject cross region
					var_ratio_dir = mask_dir + 'run_' + str(run) + '_linear_regression_ratio.txt'
					var_ratio = float(np.loadtxt(var_ratio_dir))
					corr_ratio = 0
					if not ceil == 0:
						corr_ratio = var_ratio / ceil # calculate correlation ratio in respect to within region ratio
					# save ceil correlation ratio to file
					with open(out_dir, 'w+') as outfile:
							outfile.write(str(corr_ratio))