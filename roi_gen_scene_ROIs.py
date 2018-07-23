# generate scene rois by picking top 80 voxels in the generated sphere
import os, math
import nibabel as nib
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04', 'sub-05']
### all_masks_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_masks = ['rPC', 'rPPA', 'rTOS'] # general mask
masks = [] # list of all general mask data
anat_thr = 1 # threshold of anatomical data 
final_voxel_count = 80 # total number of voxels needed for each ROI
final_mask_name = '' # mask output file name
mask_data_affine = 0

# cd to working directory
os.chdir(work_dir)
# load masks data
for mask_index in range(0, len(all_masks)):
	cur_mask_dir = all_masks_dir + all_masks[mask_index] + '.nii.gz'
	cur_mask = nib.load(cur_mask_dir)
	mask_data_affine = cur_mask.affine
	cur_mask = cur_mask.get_data()
	cur_mask = np.squeeze(cur_mask) # shrink dimension to 3
	masks.append(cur_mask)

# iterate through all subjects to create rois
for i in range(0, len(all_subjects)): # iterate through all subjects
	# initialization info
	subject = all_subjects[i]
	sub_dir = work_dir + subject + '_complete/'
	out_dir = sub_dir + subject + '_ROIs/'
	# create output directory if not exists
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	# load data and masks
	zstat4_dir = sub_dir + subject + '_feat.feat/stats/zstat4.nii.gz'
	zstat4_data = nib.load(zstat4_dir).get_data()
	zstat4_data_shape = zstat4_data.shape
	anat_dir = out_dir + subject + '_T1w_MNI152_funcSize.nii.gz'
	anat_data = nib.load(anat_dir).get_data()

	# iterate through 3 kinds of masks
	for j in range(0, len(all_masks)):	
		# initiate info
		mask_data = masks[j]
		final_mask = np.zeros(masks[j].shape) # final mask of ROI

		# iterate through zstat data and find peak voxel in current mask
		max_x, max_y, max_z = 0, 0, 0
		for x in range(0, zstat4_data_shape[0]):
			for y in range(0, zstat4_data_shape[1]):
				for z in range(0, zstat4_data_shape[2]):
					if mask_data[x, y, z] == 1 and zstat4_data[x, y, z] > zstat4_data[max_x, max_y, max_z]:
						max_x = x
						max_y = y
						max_z = z

		# mark peak as true in masks
		final_mask[max_x, max_y, max_z] = 1

		# save all voxels in/around sphere to list for sorting
		max_list = []
		for x in range(max_x - 6, max_x + 6):
			for y in range(max_y - 6, max_y + 6):
				for z in range(max_z - 6, max_z + 6):
					if mask_data[x, y, z] == 1 and anat_data[x, y, z] >= anat_thr:
						max_list.append(zstat4_data[x, y, z])

		# sort list and pick the top 80 for final mask, intersecting with sphere and anat data
		max_list.sort(reverse = True)
		max_list = max_list[:final_voxel_count]
		for x in range(max_x - 6, max_x + 6):
			for y in range(max_y - 6, max_y + 6):
				for z in range(max_z - 6, max_z + 6):
					if mask_data[x, y, z] == 1 and anat_data[x, y, z] >= anat_thr and zstat4_data[x, y, z] in max_list:
						final_mask[x, y, z] = 1
						index = max_list.index(zstat4_data[x, y, z]) # index of current voxel
						del max_list[index] # remove the value from max_list to avoid repeating value
						# print(len(max_list))

		# through warning if the mask is too small
		if len(max_list) >= 20:
			print('warning: mask too small -- ' + final_mask_name)
			print(final_voxel_count - len(max_list))

		# save final mask as nifti file
		final_mask_name = all_masks[j] + '_final_mask_' + subject + '_bin.nii.gz'
		final_mask_img = nib.Nifti1Image(final_mask, mask_data_affine)
		nib.save(final_mask_img, out_dir + final_mask_name)
