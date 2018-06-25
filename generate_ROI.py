import os, math
import nibabel as nib
import numpy as np

main_directory = '/Users/chloe/Documents/'
os.chdir(main_directory)

# load zstat data and mask
data = nib.load('./zstat3_sub-18.nii.gz')
mask = nib.load('./TPmask_R_funcSize_bin.nii.gz')
mask_affine = mask.affine
data = data.get_data()
mask = mask.get_data()
data_shape = data.shape
mask_shape = mask.shape

# initiate final mask
final_mask = np.zeros(mask_shape)
temp_mask = np.zeros(mask_shape)

# iterate through data and find peak
max_x, max_y, max_z = 0, 0, 0
for x in range(0, data_shape[0]):
	for y in range(0, data_shape[1]):
		for z in range(0, data_shape[2]):
			if mask[x, y, z] == 1 and data[x, y, z] > data[max_x, max_y, max_z]:
				max_x = x
				max_y = y
				max_z = z

# mark peak as true
temp_mask[max_x, max_y, max_z] = 1
final_mask[max_x, max_y, max_z] = 1

# make a sphere around the peak
r = 9 # radius of sphere in mm
x_mm = 2.8 # mm in each voxel x dimension
y_mm = 2.831168831168831 # mm in each voxel y dimension
z_mm = 3.033333333333333 # mm in each voxel z dimension
for x in range(max_x - 4, max_x + 4):
	for y in range(max_y - 4, max_y + 4):
		for z in range(max_z - 4, max_z + 4):
			distance = math.sqrt(math.pow((max_x - x) * x_mm, 2) + math.pow((max_y - y) * y_mm, 2) + math.pow((max_z - z) * z_mm, 2))
			if distance <= r + 2.5:
				temp_mask[x, y, z] = 1

# select max 80 voxels to be the real mask
count = 80
max_list = []
for x in range(max_x - 4, max_x + 4):
	for y in range(max_y - 4, max_y + 4):
		for z in range(max_z - 4, max_z + 4):
			if mask[x, y, z] == 1 and temp_mask[x, y, z] == 1:
				max_list.append(data[x, y, z])

max_list.sort(reverse = True)
max_list = max_list[:count]
for x in range(max_x - 4, max_x + 4):
	for y in range(max_y - 4, max_y + 4):
		for z in range(max_z - 4, max_z + 4):
			if temp_mask[x, y, z] == 1 and data[x, y, z] in max_list:
				final_mask[x, y, z] = 1

# save final mask as nifti file
final_mask_img = nib.Nifti1Image(final_mask, mask_affine)
nib.save(final_mask_img, main_directory + 'final_mask.nii.gz')


