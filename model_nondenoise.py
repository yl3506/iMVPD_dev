import os, json
import nibabel as nib
import numpy as np
from sklearn import linear_model

# initialize parameters
work_dir = '/Users/chloe/Documents/'
main_out_dir = '/Users/chloe/Documents/output_nondenoise/'
all_subjects = ['sub-19', 'sub-20']
all_masks = ['rATL', 'rFFA', 'rOFA', 'rSTS']
### work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
### main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_nondenoise/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
total_run = 8

# create output folder if not exists
if not os.path.exists(main_out_dir):
	os.makedirs(main_out_dir)

# cd to work directory
os.chdir(work_dir)

# iterate through all combinations of subjects
for sub_1_index in range(0, len(all_subjects) - 1):
	sub_1 = all_subjects[sub_1_index]
	for sub_2_index in range(sub_1_index + 1, len(all_subjects)):
		sub_2 = all_subjects[sub_2_index]
		# iterate through 2 directions of modeling
		for direction_index in range(0, 2): 
			sub_1_dir = ''
			sub_2_dir = ''
			out_dir = ''
			if direction_index == 1:
				# model of inversed direction
				sub_temp = sub_1
				sub_1 = sub_2
				sub_2 = sub_temp
			# initialize data info	
			out_dir = main_out_dir + sub_1 + '_to_' + sub_2 + '/'
			sub_1_dir = work_dir + sub_1 + '_complete/' 
			sub_2_dir = work_dir + sub_2 + '_complete/'
			sub_1_data_dir = sub_1_dir + 'ses-movie/func/'
			sub_2_data_dir = sub_2_dir + 'ses-movie/func/'
			if not os.path.exists(out_dir):
				os.makedirs(out_dir)

			# iterate through combination of 4 masks
			for mask_1_index in range(0, len(all_masks) - 1):
				mask_1 = all_masks[mask_1_index]
				for mask_2_index in range(mask_1_index + 1, len(all_masks)):
					mask_2 = all_masks[mask_2_index]
					# iterate through two directions of mask pair
					for mask_direction in range(0, 2):
						mask_1_dir = ''
						mask_2_dir = ''
						mask_out_dir = ''
						if mask_direction == 1:
							# interchange masks
							mask_temp = mask_1
							mask_1 = mask_2
							mask_2 = mask_1
						# initialize data info
						mask_out_dir = out_dir + mask_1 + '_to_' + mask_2 + '/'
						mask_1_dir = sub_1_dir + sub_1 + '_ROIs/'
						mask_2_dir = sub_2_dir + sub_2 + '_ROIs/'
						mask_1_data_dir = sub_1_dir + sub_1 + '_ROIs/' + mask_1 + '_final_mask_' + sub_1 + '_bin.nii.gz'
						mask_2_data_dir = sub_2_dir + sub_2 + '_ROIs/' + mask_2 + '_final_mask_' + sub_2 + '_bin.nii.gz'
						if not os.path.exists(mask_out_dir):
							os.makedirs(mask_out_dir)
						# load mask data
						mask_1_data = nib.load(mask_1_data_dir).get_data()
						mask_2_data = nib.load(mask_2_data_dir).get_data()
						mask_1_data_shape = mask_1_data.shape
						mask_2_data_shape = mask_2_data.shape
						
						# iterate through all runs
						for run in range(1, total_run + 1):
							# load movie data current run
							sub_1_data = nib.load(sub_1_data_dir + sub_1 + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz').get_data()
							sub_2_data = nib.load(sub_2_data_dir + sub_2 + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz').get_data()
							sub_1_data_shape = sub_1_data.shape
							sub_2_data_shape = sub_2_data.shape
							# initialize matrix data, a and b might be of different shpe
							mask_1_num = int(np.sum(mask_1_data))
							mask_2_num = int(np.sum(mask_2_data))
							print(type(mask_1_num))
							matrix_1 = np.zeros((sub_1_data_shape[3], mask_1_num))
							matrix_2 = np.zeros((sub_2_data_shape[3], mask_2_num))
							
							# iterate through sub_1_data with mask_1
							index_1 = 0 # column index, corresponding to each voxel in mask
							for t in range(0, sub_1_data_shape[3]): # row index, time point
								# matrix_1[t, index_1] = 1 # bias term
								for x in range(0, sub_1_data_shape[0]):
									for y in range(0, sub_1_data_shape[1]):
										for z in range(0, sub_1_data_shape[2]):
											# if mask true, take value into matrix
											if mask_1_data[x, y, z] == 1:
												matrix_1[t, index_1] = sub_1_data[x, y, z, t]
												index_1 += 1
								index_1 = 0
							
							# iterate through sub_2_data with mask_2
							index_2 = 0 # column index, corresponding to each voxel in mask
							for t in range(0, sub_2_data_shape[3]): # row index, time point
								# matrix_1[t, index_1] = 1 # bias term
								for x in range(0, sub_2_data_shape[0]):
									for y in range(0, sub_2_data_shape[1]):
										for z in range(0, sub_2_data_shape[2]):
											# if mask true, take value into matrix
											if mask_2_data[x, y, z] == 1:
												matrix_2[t, index_1] = sub_2_data[x, y, z, t]
												index_2 += 1
								index_2 = 0

							# linear regression step
							train_1 = matrix_1[:sub_1_data_shape[3] - 50, :]
							test_1 = matrix_1[sub_1_data_shape[3] - 50:, :]
							train_2 = matrix_2[:sub_2_data_shape[3] - 50, :]
							test_2 = matrix_2[sub_2_data_shape[3] - 50:, :]
							# fit into linear regression model
							linear = linear_model.LinearRegression()
							linear.fit(train_1, train_2)
							# print('linear regression coefficients :')
							# print(linear.coef_)
							# computer error
							predict_lin = linear.predict(test_1)
							err_lin = predict_lin - test_2
							print('linear regression squared error: %f' % np.sum(err_lin * err_lin))
							print('linear regression test_2 square : %f' % np.sum(test_2 * test_2))

							# save prediction to file
							predict_lin_tolist = predict_lin.tolist()
							out_file = mask_out_dir + 'run_' + str(run) + '_linear_regression_predict.json' 
							with open(out_file, 'w+') as outfile:
								json.dump(predict_lin_tolist, outfile)
							with open(out_file, 'a+') as outfile:
								json.dump('linear regression squared error: %f' % np.sum(err_lin * err_lin), outfile)
								json.dump('linear regression test_2 square : %f' % np.sum(test_2 * test_2), outfile)














