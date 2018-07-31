## make an average mask for zstat4 data of all subjects
import os
import nibabel as nib
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04', 'sub-05']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
out_dir = work_dir + 'ztsat4_average.nii.gz'

# cd to work directory
os.chdir(work_dir)
data_affine = 0
data = 0
first_flag = True

# load the header info
for sub_index in range(0, len(all_subjects)):
	# initialize info
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_complete/'
	data_dir = sub_dir + subject + '_feat.feat/stats/zstat4.nii.gz'
	cur_data = nib.load(data_dir)
	# increment data
	if first_flag:
		data_affine = cur_data.affine
		data = cur_data.get_data()
		first_flag = False
	else:
		cur_data = cur_data.get_data()
		data += cur_data

# take the average of data
data = data / len(all_subjects)
# save data to nifti file
data_img = nib.Nifti1Image(data, data_affine)
nib.save(data_img, out_dir)