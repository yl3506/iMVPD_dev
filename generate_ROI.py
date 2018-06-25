import os 
import nibabel as nib
import numpy as np

main_directory = ''
os.chdir(main_directory)

# load zstat data and mask
data = nib.load('/Users/chloe/Documents/zstat3_sub-18.nii.gz')
mask = nib.load('/Users/chloe/Documents/TPmask_R_funcSize_bin.nii.gz')
data = data.get_data()
mask = mask.get_data()
data_shape = data.shape
mask_shape = mask.shape

# initiate final mask
final_mask = np.zeros(mask_shape)

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
final_mask[max_x, max_y, max_z] = 1

# make a sphere around the peak
r = 9 # radius of sphere in mm
x_mm = 2.8 # mm in each voxel x dimension
y_mm = 2.831168831168831 # mm in each voxel y dimension
z_mm = 3.033333333333333 # mm in each voxel z dimension
for 

# select max 80 voxels to be the real mask

