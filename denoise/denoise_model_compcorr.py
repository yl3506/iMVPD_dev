## use PCA and linear regression to model noise (WM & CSF) after decosine, and extract real brain data
import os, json, time
import nibabel as nib
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model

# initalize data
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']
rois = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
n_pc = 5

# iterate through all subjects
for sub in all_subjects:
	# initialize data
	sub_dir = work_dir + sub + '_complete/'
	sub_out_dir = sub_dir + sub + '_decosed_deglobal_compcorr/'
	noise_dir = sub_dir + sub + '_pre/'
	roi_dir = sub_dir + sub + '_decosed_deglobal/'
	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	
	# load the data from all runs
	for run in range(1, total_run + 1):		
		# get noise data
		noise_data = np.load(noise_dir + sub + '_noise_run_' + str(run) + '.npy').T # v x t
		# get roi data
		roi_data = []
		first_flag = True
		roi_len = np.zeros(len(rois))
		for m in range(0, len(rois)):
			roi_tmp = np.load(roi_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_deglobal.npy').T # v x t
			if first_flag:
				roi_data = roi_tmp
				first_flag = False
			else:
				roi_data = np.concatenate((roi_data, roi_tmp)) # v x t
			roi_len[m] = roi_tmp.shape[0]

		# do PCA on the mask_data
		pca = PCA(n_components = n_pc)
		noise_data = noise_data.T # t x v
		pca.fit(noise_data)
		mask_pc = pca.fit_transform(noise_data) # get principal components, t x 5
		roi_data = np.transpose(roi_data) # t x v
		
		# linear regression on each voxel: PCs -> voxel pattern
		linear = linear_model.LinearRegression()
		linear.fit(mask_pc, roi_data)

		# predict the activity of each voxel for this run 
		predict = linear.predict(mask_pc)
		brain_real = roi_data - predict # t x v
		brain_real = np.transpose(brain_real) # v x t

		# split data into different rois
		len_count = 0
		for m in range(0, len(rois)):
			cur_noise = (brain_real[len_count: len_count + int(roi_len[m]), :]).T
			len_count += int(roi_len[m])
			# save real data into file
			out_file = sub_out_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_decosed_deglobal_compcorr.npy'
			np.save(out_file, cur_noise)
