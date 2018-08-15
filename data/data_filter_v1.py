## filter out v1 data from masks
import os, json, time, pickle
import nibabel as nib
import numpy as np
from sklearn import linear_model
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
mask_dir = '/mindhive/saxelab3/anzellotti/forrest/rV1_mask_funcSize_bin.nii.gz'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
mask = 'rV1'
total_run = 8

# cd to work directory
os.chdir(work_dir)
mask_data = nib.load(mask_dir).get_data()

# preprocess data: filter movie data with rois for all subjects
for s in range(0, len(all_subjects)):
	# data initialize
	sub = all_subjects[s]
	sub_dir = work_dir + sub + '_complete/'
	sub_data_dir = sub_dir + 'ses-movie/func/'
	pre_out_dir = sub_dir + sub + '_pre/'
	# make output dir if not exist
	if not os.path.exists(pre_out_dir):
		os.makedirs(pre_out_dir)

	# iterate through all runs of this subject and filter by roi masks
	for run in range(1, total_run + 1):
		run_dir = sub_data_dir + sub + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz'
		run_data = nib.load(run_dir).get_data()
		roi_out_dir = pre_out_dir + sub + '_' + mask + '_run_' + str(run) + '.npy'
		roi_data = np.zeros((run_data.shape[3], int(np.sum(mask_data))))

		# iterate through all voxels to find roi voxels
		roi_index = 0
		for t in range(0, run_data.shape[3]):
			for x in range(0, run_data.shape[0]):
				for y in range(0, run_data.shape[1]):
					for z in range(0, run_data.shape[2]):
						if mask_data[x, y, z] == 1:
							roi_data[t, int(roi_index)] = run_data[x, y, z, t]
							roi_index += 1
			roi_index = 0 # to next row, reset column indices

		# save roi data
		np.save(roi_out_dir, roi_data)