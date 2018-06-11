# load data from nisti files
# and generate regions of interests based on localizer/mask
import os
import nibabel as nib
import master as mst
import numpy as np

# load the directories and current subject number
data_dir = mst.data_directory
os.chdir(data_dir)


img = nib.load("input.nii.gz")
matrix = np.zeros(img.shape)
new_img = nib.Nifti1Image(matrix, img.affine, img.header)
nb.save(new_img, "output.nii.gz")
