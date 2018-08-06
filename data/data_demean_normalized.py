# demean denoised data to make the mean at zero
import os, json, time
import nibabel as nib
import numpy as np

# initalize data
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']

# iterate through all subjects
for sub in all_subjects:

	# initialize data
	sub_dir = work_dir + sub + '_complete/'
	sub_out_dir = sub_dir + sub + '_decosed_deglobal_normalized_demean/'
	data_dir = sub_dir + sub + '_decosed_deglobal_normalized/'
	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	
	# load data 
	os.chdir(data_dir)
	# iterate through all data files
	for file in os.listdir(data_dir):
		data = np.load(data_dir + file)
		data_final = np.zeros(data.shape) # initialize output matrix
		# iterate through all voxels to demean
		for v in range(0, data.shape[1]):
			voxel = data[:, v]
			v_mean = np.mean(voxel)
			data_final[:, v] = data[:, v] - v_mean
		# write output file
		out_file = sub_out_dir + file
		np.save(out_file, data_final)
