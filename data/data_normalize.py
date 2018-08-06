## normalize denoised data to be of the same scale
import os
import numpy as np

# initalize data
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']
rois = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8

# iterate through all subjects
for sub in all_subjects:
	
	# initialize info
	sub_dir = work_dir + sub + '_complete/'
	real_dir = sub_dir + sub + '_decosed_deglobal_compcorr/'
	real_out_dir = sub_dir + sub + '_decosed_deglobal_compcorr_normalized/'
	if not os.path.exists(real_out_dir):
		os.makedirs(real_out_dir)
	
	# iterate through all runs
	for run in range(1, total_run + 1):
		# iterate through all masks
		for m in range(0, len(rois)):
			# load data of real
			real_data = np.load(real_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_deglobal_compcorr.npy')
			real_data_norm = np.zeros(real_data.shape)
			
			# remove the mean of each voxel
			for v in range(0, real_data.shape[1]):
				real_mean = np.mean(real_data[:, v])
				real_data_norm[:, v] = real_data[:, v] - real_mean
			
			# calculate the range of 90% of the data
			real_max = np.percentile(real_data_norm, 95)
			real_min = np.percentile(real_data_norm, 5)
			real_range = real_max - real_min

			# calculate the activity ratio of real
			real_data_norm = (real_data_norm - real_min) / real_range

			# save data to file
			np.save(real_out_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_deglobal_compcorr_normalized.npy', real_data_norm)

