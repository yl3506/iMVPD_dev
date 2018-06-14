import os
import nibabel as nib
import numpy as np
# load data
os.chdir('/Users/chloe/Documents/data_test/')
mask = nib.load('aal.nii.gz')
mask_data = mask.get_data()
img = nib.load('sub-rid000001_task-beh_run-1_bold_space-MNI152NLin2009cAsym_preproc.nii.gz')
img_data = img.get_data()
print("mask_data shape")
print(mask_data.shape)
print("img_data shape")
print(img_data.shape)

# rearrange: select sub-array of mask to match shape of img
mask_data=mask_data[50:115,100:177,80:145]
print("mask_data shape after rearrangement")
print(mask_data.shape)
# check number of voxels with certain label
mask_a_label = 79
print("number of label 79") # 316
num_label_a = np.count_nonzero(mask_data==mask_a_label)
print(num_label_a)
mask_b_label = 2
print("number of label 2") # 1383
num_label_b = np.count_nonzero(mask_data==mask_b_label)
print(num_label_b)

# generate mask
mask_a = mask_data == mask_a_label
mask_b = mask_data == mask_b_label

# apply mask on img_data
a = np.zeros((196,num_label_a+1)) # initialize region a
b = np.zeros((196,num_label_b)) # initialize region b
# iterate through img_data with mask
a_index = 0
b_index = 0
for t in range(0, 196):
	a[t, a_index] = 1 # bias term
	a_index += 1
	for x in range(0, 65):
		for y in range(0, 77):
			for z in range(0, 65):
				if mask_a[x,y,z]: # if mask true
					print("xyzt, a_index: ")
					print(x)
					print(y)
					print(z)
					print(t)
					print(a_index)
					a[t, a_index] = img_data[x,y,z,t]
					a_index += 1
				elif mask_b[x,y,z]:
					print("xyzt, b_index: ")
					print(x)
					print(y)
					print(z)
					print(t)
					print(b_index)
					b[t, b_index] = img_data[x,y,z,t]
					b_index += 1				
	a_index = 0 # reset column index
	b_index = 0


# check if region data is correctly masked
print(a)
print(b)


