import os, json
import nibabel as nib
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model
from scipy import ndimage

# initalize data
### work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
### main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_denoise/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
work_dir = '/Users/chloe/Documents/'
main_out_dir = '/Users/chloe/Documents/output_denoise/'
all_subjects = ['sub-18']
masks = ['_T1w_space-MNI152NLin2009cAsym_class-CSF_probtissue.nii.gz', '_T1w_space-MNI152NLin2009cAsym_class-WM_probtissue.nii.gz']
mask_thr = 0.5
shrink_size = 1 # shrink mask by this amount of voxels on the boundary
total_run = 8
n_pc = 5
if not os.path.exists(main_out_dir):
	os.makedirs(main_out_dir)


# iterate through all subjects
for sub in all_subjects:

	# generate union mask
	# initialize info
	sub_dir = work_dir + sub + '_complete/'
	mask_dir = sub_dir + 'anat/'
	sub_out_dir = main_out_dir + sub + '_denoise/'
	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	# load masks
	mask_CSF = nib.load(mask_dir + sub + masks[0])
	mask_WM = nib.load(mask_dir + sub + masks[1])
	mask_CSF_affine = mask_CSF.affine
	mask_WM_affine = mask_WM.affine
	mask_CSF = mask_CSF.get_data()
	mask_WM = mask_WM.get_data() # mask CSF and WM should be of same shape
	# make union of the two masks, filter with threshold
	mask_union = np.zeros(mask_CSF.shape)
	for x in range(0, mask_CSF.shape[0]):
		for y in range(0, mask_CSF.shape[1]):
			for z in range(0, mask_CSF.shape[2]):
				if mask_CSF[x, y, z] >= mask_thr or mask_WM[x, y, z] >= mask_thr:
					mask_union[x, y, z] = 1
	# shrink the mask
	mask_union = ndimage.binary_erosion(mask_union, iterations = shrink_size).astype(int)
	# save the shrinked mask somewhere
	mask_union_img = nib.Nifti1Image(mask_union, mask_CSF_affine)
	nib.save(mask_union_img, sub_out_dir + sub + '_CSF_WM_mask_union_bin_shrinked.nii.gz')
	

	# load the data from all runs
	for run in range(1, total_run + 1):

		print('run number: ' + str(run))
		
		# initialize data
		run_dir = sub_dir + 'ses-movie/func/' + sub + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz'
		run_data = nib.load(run_dir).get_data()
		brain_data = np.zeros(((run_data.shape[0] * run_data.shape[1] * run_data.shape[2] - np.sum(mask_union)), run_data.shape[3]))
		mask_data = np.zeros((np.sum(mask_union), run_data.shape[3]))
		
		print('shape of brain_data: ')
		print(brain_data.shape)
		print('shape of mask_data: ')
		print(mask_data.shape)

		# load data to whole brain matrix and mask matrix
		for t in range(0, run_data.shape[3]):
			row_count_brain = 0
			row_count_mask = 0
			for x in range(0, run_data.shape[0]):
				for y in range(0, run_data.shape[1]):
					for z in range(0, run_data.shape[2]):
						if mask_union[x, y, z] == 1:
							mask_data[row_count_mask, t] = run_data[x, y, z, t]
							row_count_mask += 1
						else:
							brain_data[row_count_brain, t] = run_data[x, y, z, t]
							row_count_brain += 1
		
		# do PCA on the mask_data
		mask_pc = PCA(n_components = n_pc).fit(mask_data).components_ # get principal components

		print('shape of mask_pc: ')
		print(mask_pc.shape)

		# linear regression on each voxel: PCs -> voxel pattern
		weight = np.empty((n_pc, (run_data.shape[0] * run_data.shape[1] * run_data.shape[2] - np.sum(mask_union))))
		weight_tr = np.transpose(weight)

		print('shape of initialized weight_tr: ')
		print(weight_tr.shape)
		
		weight_tr = np.matmul(brain_data, np.linalg.pinv(mask_pc)) # pseudo inverse

		print('shape of pca-modeled weight_tr: ')
		print(weight_tr.shape)

		# predict the activity of each voxel for this run 
		predict = np.matmul(weight_tr, mask_pc)
		brain_real = brain_data - predict

		# save real data into file
		brain_real_tolist = brain_real.tolist()
		out_file = sub_out_dir + '_run_' + str(run) + '_brain_real.json'
		with open(out_file, 'w+') as outfile:
			json.dump(brain_real_tolist, outfile, indent = 4)


