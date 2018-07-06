import os, json, time
import nibabel as nib
import numpy as np
from sklearn.decomposition import PCA
from sklearn import linear_model

# initalize data
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
### work_dir = '/Users/chloe/Documents/'
all_subjects = ['sub-02', 'sub-03']
mask = '_CSF_WM_mask_union_bin_shrinked_funcSize.nii.gz'
rois = ['rATL', 'rFFA', 'rOFA', 'rSTS']
total_run = 8
n_pc = 5

# iterate through all subjects
for sub in all_subjects:

	# initialize data
	sub_dir = work_dir + sub + '_complete/'
	sub_out_dir = sub_dir + sub + '_denoised/'
	noise_dir = sub_dir + sub + '_pre/'

	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	
	# load the data from all runs
	for run in range(1, total_run + 1):

		print('run number: ' + str(run))
		
		# get noise data
		noise_data = np.load(noise_dir + sub + '_noise_run_' + str(run) + '.npy').T

		# get roi data
		roi_dir = sub_dir + sub + '_pre/'
		roi_data = []
		first_flag = True
		roi_len = np.zeros(len(rois))
		for m in range(0, len(rois)):
			roi_tmp = np.load(roi_dir + sub + '_' + rois[m] + '_run_' + str(run) + '.npy').T
			if first_flag:
				roi_data = roi_tmp
				first_flag = False
			else:
				roi_data = np.concatenate((roi_data, roi_tmp))
			roi_len[m] = roi_tmp.shape[0]
			print('roi_tmp shape after transpose:')
			print(roi_tmp.shape)
			print('roi_data shape after transpose:')
			print(roi_data.shape)
			print('roi_len: ' + str(roi_len[m]))
		
		t1 = time.time()
		print('ready to do PCA')

		# do PCA on the mask_data
		mask_pc = PCA(n_components = n_pc).fit(noise_data).components_ # get principal components
		mask_pc = np.transpose(mask_pc) # t x 5
		roi_data = np.transpose(roi_data) # t x v

		print('pca finished\nshape of mask_pc: ')
		print(mask_pc.shape)

		# linear regression on each voxel: PCs -> voxel pattern
		print('linear regression step')
		linear = linear_model.LinearRegression()
		linear.fit(mask_pc, roi_data)

		print('fitting finished')
		# predict the activity of each voxel for this run 
		predict = linear.predict(mask_pc)
		brain_real = roi_data - predict # t x v
		brain_real = np.transpose(brain_real) # v x t
		print("brain_real shape after transpose v x t: ")
		print(brain_real.shape)
		
		# weight = np.empty((n_pc, np.sum(roi_mask)))
		# weight_tr = np.transpose(weight)

		# print('shape of initialized weight_tr: ')
		# print(weight_tr.shape)
		
		# weight_tr = np.matmul(brain_data, np.linalg.pinv(mask_pc)) # pseudo inverse

		# print('shape of pca-modeled weight_tr: ')
		# print(weight_tr.shape)

		# # predict the activity of each voxel for this run 
		# predict = np.matmul(weight_tr, mask_pc)
		# brain_real = brain_data - predict

		len_count = 0
		# split data into different rois
		for m in range(0, len(rois)):
			cur_noise = (brain_real[len_count: len_count + int(roi_len[m]), :]).T
			len_count += int(roi_len[m])
			print(len_count)
			print('predict_all number ' + str(m) + '\nshape: ')
			print(cur_noise.shape)
			# save real data into file
			out_file = sub_out_dir + sub + '_' + rois[m] + '_run_' + str(run) + '_real.npy'
			np.save(out_file, cur_noise)
