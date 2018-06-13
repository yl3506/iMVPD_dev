# load data from nifti files
# and generate regions of interests based on localizer/mask
import os
import nibabel as nib
import numpy as np

# load data
img = nib.load("input.nii.gz")
matrix = np.zeros(img.shape)
new_img = nib.Nifti1Image(matrix, img.affine, img.header)
nib.save(new_img, "output.nii.gz")
