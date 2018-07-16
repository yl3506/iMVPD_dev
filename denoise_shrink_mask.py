# generate noise mask and shrink by 1 voxel on the surface
import os, json
import nibabel as nib
import numpy as np
from scipy import ndimage

# initalize data
### work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
work_dir = '/Users/chloe/Documents/'
all_subjects = ['sub-01']
masks = ['_T1w_space-MNI152NLin2009cAsym_class-CSF_probtissue.nii.gz', '_T1w_space-MNI152NLin2009cAsym_class-WM_probtissue.nii.gz']
mask_thr = 0.5
shrink_size = 1 # shrink mask by this amount of voxels on the boundary

# iterate through all subjects
for sub in all_subjects:

	# generate union mask
	# initialize info
	sub_dir = work_dir + sub + '_complete/'
	mask_dir = sub_dir + 'anat/'
	sub_out_dir = work_dir + sub + '_complete/' + sub + '_ROIs/'
	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	# load masks
	mask_CSF = nib.load(mask_dir + sub + masks[0])
	mask_WM = nib.load(mask_dir + sub + masks[1])
	mask_CSF_affine = mask_CSF.affine
	mask_WM_affine = mask_WM.affine
	mask_CSF_header = mask_CSF.header
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
	mask_union_img = nib.Nifti1Image(mask_union, mask_CSF_affine, mask_CSF_header)
	nib.save(mask_union_img, sub_out_dir + sub + '_CSF_WM_mask_union_bin_shrinked.nii.gz')
	