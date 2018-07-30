## use PCA and linear regression to model confound xyz after decosine, and extract real brain data
import os, json, time
import nibabel as nib
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model

# initalize data
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04', 'sub-05']
rois = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8

# iterate through all subjects
for sub in all_subjects:
	
	# initialize data
	sub_dir = work_dir + sub + '_complete/'
	sub_out_dir = sub_dir + sub + '_decosed_dexyz_2/'
	noise_dir = sub_dir + sub + '_xyz/' # directory of confound files
	roi_dir = sub_dir + sub + '_decosed_2/'
	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	
	# load the data from all runs
	for run in range(1, total_run + 1):		

		# get noise data
		noise_data = np.load(noise_dir + sub + '_run_' + str(run) + '_xyz.npy') # t x c
		# get roi data
		roi_data = []
		first_flag = True
		roi_len = np.zeros(len(rois))
		for m in range(0, len(rois)):
			roi_tmp = np.load(roi_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed.npy').T # v x t
			if first_flag:
				roi_data = roi_tmp
				first_flag = False
			else:
				roi_data = np.concatenate((roi_data, roi_tmp)) # 2v x t
			roi_len[m] = roi_tmp.shape[0]

		# linear regression on each voxel: xyz -> roi pattern
		roi_data = roi_data.T # t x v
		linear = linear_model.LinearRegression()
		linear.fit(noise_data, roi_data)

		# predict the activity of each voxel for this run 
		predict = linear.predict(noise_data) # t x v
		brain_real = roi_data - predict # t x v
		brain_real = np.transpose(brain_real) # v x t

		# split data into different rois
		len_count = 0
		for m in range(0, len(rois)):
			cur_real = (brain_real[len_count: len_count + int(roi_len[m]), :]).T # t x v
			len_count += int(roi_len[m])
			# save real data into file
			out_file = sub_out_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_dexyz.npy'
			np.save(out_file, cur_real)
