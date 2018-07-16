# generate one principal component for each of the denoised data
import os
import numpy as np
from sklearn.decomposition import PCA

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-03']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rATL', 'rFFA', 'rOFA', 'rSTS']
total_run = 8

# iterate through all combinations of subjects (including within subject)
for sub_index in range(0, len(all_subjects)):
	sub = all_subjects[sub_index]
	sub_dir = work_dir + sub + '_complete/'
	data_dir = sub_dir + sub + '_denoised_normalized_demean/'
	out_dir = sub_dir + sub + '_pc/'
	# create output dir if not exists
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	# iterate through all masks
	for mask_index in range(0, len(all_masks)):
		# initialize data info for this mask
		mask = all_masks[mask_index]
		# process the first run to get pca matrix
		data = np.load(data_dir + sub + '_' + mask + '_run_1_real_normalized.npy')
		pca = PCA(n_components=1)
		pca.fit(data)
		mask_pc = pca.fit_transform(data)
		print('mask_pc shape: ')
		print(mask_pc.shape) # should be of v x 1
		mask_pc_matrix = pca.components_.T # v x 1
		np.save(out_dir + sub + '_' + mask + '_run_1_pc.npy', mask_pc)
		# iterate through the rest runs under this mask
		for run in range(2, total_run + 1):
			# get data
			run_data = np.load(data_dir + sub + '_' + mask + '_run_' + str(run) + '_real_normalized.npy')
			# transform current run data to pc
			run_pc = np.dot(run_data, mask_pc_matrix) # t x v dot v x 1
			print('run_pc shape: ')
			print(run_pc.shape) # t x 1
			# save result to file
			np.save(out_dir + sub + '_' + mask + '_run_' + str(run) + '_pc.npy', run_pc)
