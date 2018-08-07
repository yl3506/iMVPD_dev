# generate v1 roi by combining the two v1 masks
import os, math
import nibabel as nib
import numpy as np

# initialize parameters

work_directory = '/Users/chloe/Documents/'
###work_directory = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = work_directory + 'rV1_mask.nii.gz'
thr = 9

# load mask
mask1 = nib.load(work_directory + 'ProbAtlas_v4/subj_vol_all/perc_VTPM_vol_roi1_rh.nii.gz')
mask2 = nib.load(work_directory + 'ProbAtlas_v4/subj_vol_all/perc_VTPM_vol_roi2_rh.nii.gz')
mask_affine = mask1.affine
mask1 = mask1.get_data()
mask2 = mask2.get_data()

# combine two masks
mask_final = np.zeros(mask1.shape)
print(mask1.shape)
print(mask2.shape)
# iterate through all voxels
for x in range(0, mask1.shape[0]):
	for y in range(0, mask1.shape[1]):
		for z in range(0, mask1.shape[2]):
			mask_final[x, y, z] = float((mask1[x, y, z] > thr) or (mask2[x, y, z] > thr))

# save final mask
mask_final_img = nib.Nifti1Image(mask_final, mask_affine)
nib.save(mask_final_img, out_dir)