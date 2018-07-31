## normalize denoised and non-denoised data to be of the same scale
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
	real_dir = sub_dir + sub + '_decosed_compcorr/'
	pre_dir = sub_dir + sub + '_pre/'
	real_out_dir = sub_dir + sub + '_decosed_compcorr_normalized/'
	pre_out_dir = sub_dir + sub + '_pre_normalized/'
	if not os.path.exists(real_out_dir):
		os.makedirs(real_out_dir)
	if not os.path.exists(pre_out_dir):
		os.makedirs(pre_out_dir)
	
	# iterate through all runs
	for run in range(1, total_run + 1):
		# iterate through all masks
		for m in range(0, len(rois)):
			# load data of pre and real
			pre_data = np.load(pre_dir + sub + '_' + rois[m] + '_run_' + str(run) + '.npy')
			real_data = np.load(real_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_compcorr.npy')
			pre_data_norm = np.zeros(pre_data.shape)
			real_data_norm = np.zeros(real_data.shape)
			
			# remove the mean of each voxel
			for v in range(0, pre_data.shape[1]):
				pre_mean = np.mean(pre_data[:, v])
				pre_data_norm[:, v] = pre_data[:, v] - pre_mean
				real_mean = np.mean(real_data[:, v])
				real_data_norm[:, v] = real_data[:, v] - real_mean
			
			# calculate the range of 90% of the data
			pre_max = np.percentile(pre_data_norm, 95)
			pre_min = np.percentile(pre_data_norm, 5)
			pre_range = pre_max - pre_min
			real_max = np.percentile(real_data_norm, 95)
			real_min = np.percentile(real_data_norm, 5)
			real_range = real_max - real_min

			# calculate the activity ratio of pre and real
			pre_data_norm = (pre_data_norm - pre_min) / pre_range
			real_data_norm = (real_data_norm - real_min) / real_range

			# save data to file
			np.save(pre_out_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_normalized.npy', pre_data_norm)
			np.save(real_out_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_compcorr_normalized.npy', real_data_norm)

