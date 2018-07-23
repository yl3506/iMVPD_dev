## filter out roi data from masks
import os, json, time, pickle
import nibabel as nib
import numpy as np
from sklearn import linear_model
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rPC', 'rPPA', 'rTOS']
total_run = 8

# cd to work directory
os.chdir(work_dir)

# preprocess data: filter movie data with rois for all subjects
for s in range(0, len(all_subjects)):
	# data initialize
	sub = all_subjects[s]
	sub_dir = work_dir + sub + '_complete/'
	sub_data_dir = sub_dir + 'ses-movie/func/'
	sub_mask_dir = sub_dir + sub + '_ROIs/'
	pre_out_dir = sub_dir + sub + '_pre/'
	# make output dir if not exist
	if not os.path.exists(pre_out_dir):
		os.makedirs(pre_out_dir)

	# load all masks
	masks_dir = []
	masks_data = []
	for m in range(0, len(all_masks)):
		masks_dir.append(sub_mask_dir + all_masks[m] + '_final_mask_' + sub + '_bin.nii.gz')
		masks_data.append(nib.load(masks_dir[m]).get_data())

	# iterate through all runs of this subject and filter by roi masks
	for run in range(1, total_run + 1):
		run_dir = sub_data_dir + sub + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz'
		run_data = nib.load(run_dir).get_data()
		roi_out_dir = [] # each run has 4 roi_out_dir
		roi_data = [] # each run has 4 roi_data elements
		roi_indices = np.zeros(len(all_masks))
		
		# create output file and matrix
		for m in range(0, len(all_masks)):
			roi_out_dir.append(pre_out_dir + sub + '_' + all_masks[m] + '_run_' + str(run) + '.npy')
			roi_data.append(np.zeros((run_data.shape[3], int(np.sum(masks_data[m])))))

		# iterate through all voxels to find roi voxels
		for t in range(0, run_data.shape[3]):
			for x in range(0, run_data.shape[0]):
				for y in range(0, run_data.shape[1]):
					for z in range(0, run_data.shape[2]):
						for m in range(0, len(all_masks)): # check all masks
							if masks_data[m][x, y, z] == 1:
								roi_data[m][t, int(roi_indices[m])] = run_data[x, y, z, t]
								roi_indices[m] += 1
			roi_indices = np.zeros(len(all_masks)) # to next row, reset column indices

		# save roi data
		for m in range(0, len(all_masks)):
			np.save(roi_out_dir[m], roi_data[m])
