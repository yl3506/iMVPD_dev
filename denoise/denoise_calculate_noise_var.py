# calculate the variance of denoised data to make sure the extend of denoising is appropriate
import os
import numpy as np

# initalize data
### work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
work_dir = '/Users/chloe/Documents/'
all_subjects = ['sub-02', 'sub-04']
rois = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
### rois = ['rATL']
total_run = 8

# iterate through all subjects
for sub in all_subjects:
	sub_dir = work_dir + sub + '_complete/'
	real_dir = sub_dir + sub + '_decosed_compcorr/'
	pre_dir = sub_dir + sub + '_pre/'
	# iterate through all runs
	for run in range(1, total_run + 1):
		# iterate through all masks
		for m in range(0, len(rois)):
			# load denoised and non-denoised data
			real_data = np.load(real_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_compcor.npy')
			pre_data = np.load(pre_dir + sub + '_' + rois[m] + '_run_' + str(run) + '.npy')
			real_var = []
			pre_var = []
			comp_var = 0
			# calculate variance of each voxel
			for v in range(0, real_data.shape[1]):
				real_var.append(np.var(real_data[:, v]))
				pre_var.append(np.var(pre_data[:, v]))
			# calculate mean of variance
			real_var_mean = np.mean(real_var)
			pre_var_mean = np.mean(pre_var)
			comp_var = real_var_mean / pre_var_mean # compare variance
			# print result
			if comp_var < 0.25:
				print('subject ' + sub + ' run ' + str(run) + ' mask ' + rois[m] + ' comp_var ' + str(comp_var))
			