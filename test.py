import os
import nibabel as nib
import numpy as np
os.chdir('/Users/chloe/Documents/data_test/')
mask = nib.load('aal.nii.gz')
mask_data = mask.get_data()
img = nib.load('sub-rid000001_task-beh_run-1_bold_space-MNI152NLin2009cAsym_preproc.nii.gz')
img_data = img.get_data()
print("mask_data shape")
print(mask_data.shape)
print("img_data shape")
print(img_data.shape)
# rearrange