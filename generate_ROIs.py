import os, math
import nibabel as nib
import numpy as np

# initialize parameters
work_directory = '/Users/chloe/Documents/'
# work_directory = '/mindhive/saxelab3/anzellotti/forrest/'
# all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_subjects = ['sub-19']
all_masks = ['TPmask_R_funcSize_bin.nii.gz', 'ROI_rFFA_kanparcel_xyz_warped_funcSize_bin.nii.gz', 'ROI_rOFA_kanparcel_xyz_warped_funcSize_bin.nii.gz', 'wholeROI_rSTS_kanparcel_warped_funcSize_bin.nii.gz']
mask_label = 0
#all_masks_dir = ''
all_masks_dir = '/Users/chloe/Documents/kanparcel_nii/'
r = 9 # radius of sphere in mm
x_mm = 2.8 # mm in each voxel x dimension
y_mm = 2.831168831168831 # mm in each voxel y dimension
z_mm = 3.033333333333333 # mm in each voxel z dimension
final_voxel_count = 80 # total number of voxels needed for each ROI

os.chdir(work_directory)

for subject in all_subjects: # iterate through all subjects
	
	# data initialization
	sub_dir = work_directory + 'derivatives/fmriprep/' + subject + '_complete/'
	out_dir = work_directory + 'derivatives/fmriprep/' + subject + '_complete/' + subject + '_ROIs/'
	# create output directory if not exists
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	# initialize input functional data
	zstat3_dir = sub_dir + subject + '_feat.feat/stats/zstat3.nii.gz'
	zstat3_data = nib.load(zstat3_dir)
	zstat3_data = zstat3_data.get_data()
	zstat3_data_shape = zstat3_data.shape
	
	# iterate through 4 kinds of masks
	for mask in all_masks: 
		
		# data initialization
		mask_label += 1 # increment mask label number
		mask_dir = all_masks_dir + mask
		mask_data = nib.load(mask_dir) # load mask data
		mask_data = mask_data.get_data()
		mask_data_affine = mask_data.affine
		mask_data_shape = mask_data.shape
		
		# determine final mask output file name
		if mask_label == 1: 
			final_mask_name = 'rATL_final_mask_' + subject + '_bin.nii.gz'
		elif mask_label == 2:
			final_mask_name = 'rFFA_final_mask_' + subject + '_bin.nii.gz'
		elif mask_label == 3:
			final_mask_name = 'rOFA_final_mask_' + subject + '_bin.nii.gz'	
		elif mask_label == 4:
			final_mask_name = 'rSTS_final_mask_' + subject + '_bin.nii.gz'

		# initiate final mask
		final_mask = np.zeros(mask_data_shape)
		temp_mask = np.zeros(mask_data_shape)

		# iterate through zstat data and find peak voxel
		max_x, max_y, max_z = 0, 0, 0
		for x in range(0, zstat3_data_shape[0]):
			for y in range(0, zstat3_data_shape[1]):
				for z in range(0, zstat3_data_shape[2]):
					if mask_data[x, y, z] == 1 and zstat3_data[x, y, z] > stat3_data[max_x, max_y, max_z]:
						max_x = x
						max_y = y
						max_z = z

		# mark peak as true in masks
		temp_mask[max_x, max_y, max_z] = 1
		final_mask[max_x, max_y, max_z] = 1

		# make a sphere around the peak voxel
		for x in range(max_x - 4, max_x + 5):
			for y in range(max_y - 4, max_y + 5):
				for z in range(max_z - 4, max_z + 5):
					distance = math.sqrt(math.pow((max_x - x) * x_mm, 2) + math.pow((max_y - y) * y_mm, 2) + math.pow((max_z - z) * z_mm, 2))
					if distance <= r + 2.5:
						temp_mask[x, y, z] = 1

		# select max 80 voxels to be the real mask, intersection between mask and temp_mask
		max_list = []
		for x in range(max_x - 4, max_x + 5):
			for y in range(max_y - 4, max_y + 5):
				for z in range(max_z - 4, max_z + 5):
					if mask_data[x, y, z] == 1 and temp_mask[x, y, z] == 1:
						max_list.append(zstat3_data[x, y, z])

		max_list.sort(reverse = True)
		max_list = max_list[:final_voxel_count]
		for x in range(max_x - 4, max_x + 5):
			for y in range(max_y - 4, max_y + 5):
				for z in range(max_z - 4, max_z + 5):
					if temp_mask[x, y, z] == 1 and zstat3_data[x, y, z] in max_list:
						final_mask[x, y, z] = 1

		# save final mask as nifti file
		final_mask_img = nib.Nifti1Image(final_mask, mask_data_affine)
		nib.save(final_mask_img, out_dir + final_mask_name)
