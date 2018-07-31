# generate face rois by picking 80 max voxels in each sphere
import os, math
import nibabel as nib
import numpy as np

# initialize parameters

### work_directory = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-19', 'sub-20']
### all_masks_dir = '/Users/chloe/Documents/kanparcel_nii/'
work_directory = '/mindhive/saxelab3/anzellotti/forrest/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks_dir = '/mindhive/saxelab3/anzellotti/forrest/mask_tests/kanparcel_nii/'
all_masks = ['TPmask_R_funcSize_bin.nii.gz', 'ROI_rFFA_kanparcel_xyz_warped_funcSize_bin.nii.gz', 'ROI_rOFA_kanparcel_xyz_warped_funcSize_bin.nii.gz', 'wholeROI_rSTS_kanparcel_warped_funcSize_bin.nii.gz']
r = 12 # radius of sphere in mm
x_mm = 2.8 # mm in each voxel x dimension
y_mm = 2.831168831168831 # mm in each voxel y dimension
z_mm = 3.033333333333333 # mm in each voxel z dimension
anat_thr = 0.001 # threshold of anatomical data 
final_voxel_count = 80 # total number of voxels needed for each ROI
final_mask_name = '' # mask output file name

os.chdir(work_directory)

for i in range(0, len(all_subjects)): # iterate through all subjects
	
	# data initialization
	subject = all_subjects[i]
	sub_dir = work_directory + 'derivatives/fmriprep/' + subject + '_complete/'
	### sub_dir = work_directory + subject + '_complete/'
	out_dir = sub_dir + subject + '_ROIs/'
	anat_dir = out_dir + subject + '_T1w_MNI152_funcSize.nii.gz'	
	# create output directory if not exists
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	# initialize input functional data
	zstat3_dir = sub_dir + subject + '_feat.feat/stats/zstat3.nii.gz'
	zstat3_data = nib.load(zstat3_dir)
	zstat3_data = zstat3_data.get_data()
	zstat3_data_shape = zstat3_data.shape
	anat_data = nib.load(anat_dir)
	anat_data = anat_data.get_data()
	anat_data_shape = anat_data.shape
	anat_data_bin = np.zeros(anat_data_shape) # initialize binarized anat data
	# threshold the anatomical data
	for x in range(0, anat_data_shape[0]):
		for y in range(0, anat_data_shape[1]):
			for z in range(0, anat_data_shape[2]):
				if anat_data[x, y, z] >= anat_thr:
					anat_data_bin[x, y, z] = 1

	# iterate through 4 kinds of masks
	for j in range(0, len(all_masks)):

		# data initialization
		mask = all_masks[j]
		mask_dir = all_masks_dir + mask
		mask_data = nib.load(mask_dir) # load mask data
		mask_data_affine = mask_data.affine
		mask_data = mask_data.get_data()
		mask_data_shape = mask_data.shape
		prev_mask_dir = '' # previous mask to be eliminated
		prev_mask_dir_2 = ''
		prev_mask_data = []
		prev_mask_data_2 = []
		prev_mask_flag = False
		prev_mask_flag_2 = False
		
		# determine final mask output file name
		if j == 0: 
			final_mask_name = 'rATL_final_mask_' + subject + '_bin.nii.gz'
		elif j == 1:
			final_mask_name = 'rFFA_final_mask_' + subject + '_bin.nii.gz'
			prev_mask_dir = all_masks_dir + 'ROI_rOFA_kanparcel_xyz_warped_funcSize_bin.nii.gz'
			prev_mask_dir_2 = all_masks_dir + 'wholeROI_rSTS_kanparcel_warped_funcSize_bin.nii.gz'
		elif j == 2:
			final_mask_name = 'rOFA_final_mask_' + subject + '_bin.nii.gz'
			prev_mask_dir = all_masks_dir + 'ROI_rFFA_kanparcel_xyz_warped_funcSize_bin.nii.gz'	
		elif j == 3:
			final_mask_name = 'rSTS_final_mask_' + subject + '_bin.nii.gz'
			prev_mask_dir = all_masks_dir + 'ROI_rFFA_kanparcel_xyz_warped_funcSize_bin.nii.gz'
		else:
			continue

		# for debugging
		print(final_mask_name)

		# load prev mask data
		if not prev_mask_dir == '':
			prev_mask_data = nib.load(prev_mask_dir).get_data()
			prev_mask_flag = True
		if not prev_mask_dir_2 == '':
			prev_mask_data_2 = nib.load(prev_mask_dir_2).get_data()
			prev_mask_flag_2 = True
		
		# initiate final mask
		final_mask = np.zeros(mask_data_shape) # final mask of ROI
		temp_mask = np.zeros(mask_data_shape) # mask of sphere

		# iterate through zstat data and find peak voxel
		max_x, max_y, max_z = 0, 0, 0
		for x in range(0, zstat3_data_shape[0]):
			for y in range(0, zstat3_data_shape[1]):
				for z in range(0, zstat3_data_shape[2]):
					if mask_data[x, y, z] == 1 and zstat3_data[x, y, z] > zstat3_data[max_x, max_y, max_z]:
						max_x = x
						max_y = y
						max_z = z

		# mark peak as true in masks
		temp_mask[max_x, max_y, max_z] = 1
		final_mask[max_x, max_y, max_z] = 1

		# make a sphere around the peak voxel, inside mask and outside prev mask
		for x in range(max_x - 4, max_x + 5):
			for y in range(max_y - 4, max_y + 5):
				for z in range(max_z - 4, max_z + 5):
					distance = math.sqrt(math.pow((max_x - x) * x_mm, 2) + math.pow((max_y - y) * y_mm, 2) + math.pow((max_z - z) * z_mm, 2))
					if distance <= r and mask_data[x, y, z] == 1:
						if prev_mask_flag: # check if outside prev mask
							if prev_mask_data[x, y, z] == 1:
								# print('overlap with mask ' + prev_mask_dir)
								continue
							if prev_mask_flag_2:
								if prev_mask_data_2[x, y, z] == 1:
									# print('overlap with mask ' + prev_mask_dir_2)
									continue
						# else
						temp_mask[x, y, z] = 1

		# select max 80 voxels to be the real mask, intersection between mask, temp_mask, and anatomical data
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
					if temp_mask[x, y, z] == 1 and anat_data_bin[x, y, z] == 1 and zstat3_data[x, y, z] in max_list:
						final_mask[x, y, z] = 1
						index = max_list.index(zstat3_data[x, y, z]) # index of current voxel
						del max_list[index] # remove the value from max_list to avoid repeating value
						# print(len(max_list))

		# through warning if the mask is too small
		if len(max_list) >= 20:
			print('warning: mask too small -- ' + final_mask_name)
			print(final_voxel_count - len(max_list))

		# save final mask as nifti file
		final_mask_img = nib.Nifti1Image(final_mask, mask_data_affine)
		nib.save(final_mask_img, out_dir + final_mask_name)
