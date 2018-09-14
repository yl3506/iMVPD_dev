#the correlation among single denoising methods performance
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
main_dir = '/mindhive/saxelab3/anzellotti/forrest/'
work_dir = ['/mindhive/saxelab3/anzellotti/forrest/output_cos_pc3_v3/',
			'/mindhive/saxelab3/anzellotti/forrest/output_compcorr_pc3_v3/',
			'/mindhive/saxelab3/anzellotti/forrest/output_global_pc3_v3/', 
			'/mindhive/saxelab3/anzellotti/forrest/output_xyz_pc3_v3/']
denoise = ['cos', 'compcorr', 'global', 'xyz']
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
var_ratio = np.zeros((len(work_dir), len(all_masks) * (len(all_masks) - 1)))

# flatten and load all var ratio matrices
for work_dir_index in range(0, len(work_dir)):
	cur_work_dir = work_dir[work_dir_index]
	# load the var ratio chart for current denosing method
	cur_var_ratio = np.load(cur_work_dir + 'vs_' + denoise[work_dir_index] + '_pc3_v3.npy')
	cur_var_ratio = np.concatenate((np.delete(cur_var_ratio[0, :], 0), np.delete(cur_var_ratio[1, :], 1), 
		np.delete(cur_var_ratio[2, :], 2), np.delete(cur_var_ratio[3, :], 3), np.delete(cur_var_ratio[4, :], 4), 
		np.delete(cur_var_ratio[5, :], 5), np.delete(cur_var_ratio[6, :], 6)))
	# cur_var_ratio = cur_var_ratio.reshape((1, -1))
	var_ratio[work_dir_index, :] = np.squeeze(cur_var_ratio)

# calculate covariance/correlation
corr = np.corrcoef(var_ratio)
corr_out = main_dir + 'single_denoise_corr.npy'
np.save(corr_out, corr)

