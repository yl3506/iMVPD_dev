# load data from nifti files
# and generate regions of interests based on localizer/mask
import os
import nibabel as nib
import numpy as np

# load data
os.chdir('/Users/chloe/Documents/data_test/preprocessed/sub-rid000001/func')
img = nib.load("sub-rid000001_task-beh_run-1_bold_space-MNI152NLin2009cAsym_preproc.nii.gz")
img.shape
img.get_data_dtype() == np.dtype(np.int16)
data = img.get_data()
data.shape

hdr = img.header
hdr.get_xyzt_units()