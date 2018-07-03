import os, json
import nibabel as nib
import numpy as np
from sklearn import linear_model
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### main_out_dir = '/Users/chloe/Documents/output_nondenoise/'
### all_subjects = ['sub-18', 'sub-19', 'sub-20']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_nondenoise/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rATL', 'rFFA', 'rOFA', 'rSTS']
total_run = 8
regularization_flag = True # if set to fasle, do linear regression

# create output folder if not exists
if not os.path.exists(main_out_dir):
	os.makedirs(main_out_dir)

# cd to work directory
os.chdir(work_dir)

# iterate through all combinations of subjects
for sub_1_index in range(0, len(all_subjects) - 1):
	for sub_2_index in range(sub_1_index + 1, len(all_subjects)):
		sub_1 = all_subjects[sub_1_index]
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

			# print('sub_1: ' + sub_1 + ', sub_2: ' + sub_2)

			# iterate through combination of 4 masks
			for mask_1_index in range(0, len(all_masks) - 1):
				for mask_2_index in range(mask_1_index + 1, len(all_masks)):
					mask_1 = all_masks[mask_1_index]
					mask_2 = all_masks[mask_2_index]
					# print('mask_1_index: ' + str(mask_1_index) + ', mask_2_index: ' + str(mask_2_index))
					# iterate through two directions of mask pair
					for mask_direction in range(0, 2):
						mask_1_dir = ''
						mask_2_dir = ''
						mask_out_dir = ''
						if mask_direction == 1:
							# interchange masks
							mask_temp = mask_1
							mask_1 = mask_2
							mask_2 = mask_temp
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

						# print('mask_1: ' + mask_1 + ', mask_2:' + mask_2)

						
						# predict each run iteratively
						for this_run in range(1, total_run + 1):
							matrix_1_all = []
							matrix_2_all = []
							first_flag = True
							# print('this_run: ' + str(this_run))
							# collect data of all other runs
							for run in it.chain(range(1, this_run), range(this_run + 1, total_run + 1)):
								# print('run: ' + str(run))
								# load movie data current run
								sub_1_data = nib.load(sub_1_data_dir + sub_1 + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz').get_data()
								sub_2_data = nib.load(sub_2_data_dir + sub_2 + '_ses-movie_task-movie_run-' + str(run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz').get_data()
								sub_1_data_shape = sub_1_data.shape
								sub_2_data_shape = sub_2_data.shape
								# initialize matrix data, a and b might be of different shpe
								mask_1_num = int(np.sum(mask_1_data))
								mask_2_num = int(np.sum(mask_2_data))
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
								# append current run data to whole dataset
								if first_flag:
									matrix_1_all = matrix_1
									matrix_2_all = matrix_2
								else:
									matrix_1_all = np.concatenate((matrix_1_all, matrix_1))
									matrix_2_all = np.concatenate((matrix_2_all, matrix_2))
								first_flag = False
								
						
							# load movie data this_run
							sub_1_data = nib.load(sub_1_data_dir + sub_1 + '_ses-movie_task-movie_run-' + str(this_run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz').get_data()
							sub_2_data = nib.load(sub_2_data_dir + sub_2 + '_ses-movie_task-movie_run-' + str(this_run) + '_bold_space-MNI152NLin2009cAsym_preproc.nii.gz').get_data()
							sub_1_data_shape = sub_1_data.shape
							sub_2_data_shape = sub_2_data.shape
							mask_1_num = int(np.sum(mask_1_data))
							mask_2_num = int(np.sum(mask_2_data))
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
						
							# modeling step: linear regression / regularization
							# create training set and testing set
							train_1 = matrix_1_all
							train_2 = matrix_2_all
							test_1 = matrix_1
							test_2 = matrix_2

							# print('train_1 shape: ')
							# print(train_1.shape)
							# print('train_2 shape: ')
							# print(train_2.shape)
							# print('test_1 shape: ')
							# print(test_1.shape)
							# print('test_2 shape: ')
							# print(test_2.shape)

							# fit into model: regularization or linear regression
							if regularization_flag == True: # use regularization model
								# initialize and fit model
								reg = linear_model.MultiTaskElasticNetCV()
								reg.fit(train_1, train_2)
								# predict on test set, compute error
								predict_reg = reg.predict(test_1)
								err_reg = predict_reg - test_2
								# print('regularization squared error: %f' % np.sum(err_reg * err_reg))
								# print('regularization test_2 square: %f' % np.sum(test_2 * test_2))
								# write prediction to file
								predict_reg_tolist = predict_reg.tolist()
								out_file = mask_out_dir + 'run_' + str(this_run) + '_regularization_predict.json'
								with open(out_file, 'w+') as outfile:
									json.dump(predict_reg_tolist, outfile, indent = 4)
								with open(out_file, 'a+') as outfile:
									json.dump('regularization squared error: %f' % np.sum(err_reg * err_reg), outfile, indent = 4)
									json.dump('regularization test_2 square: %f' % np.sum(test_2 * test_2), outfile, indent = 4)
							else: # use linear regression model
								# initialize and fit model
								linear = linear_model.LinearRegression()
								linear.fit(train_1, train_2)						
								# predict on test set, computer error
								predict_lin = linear.predict(test_1)
								err_lin = predict_lin - test_2
								# print('linear regression squared error: %f' % np.sum(err_lin * err_lin))
								# print('linear regression test_2 square : %f' % np.sum(test_2 * test_2))							
								# write prediction to file
								predict_lin_tolist = predict_lin.tolist()
								out_file = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_predict.json' 
								with open(out_file, 'w+') as outfile:
								 	json.dump(predict_lin_tolist, outfile, indent = 4)
								with open(out_file, 'a+') as outfile:
								 	json.dump('\nlinear regression squared error: %f' % np.sum(err_lin * err_lin), outfile, indent = 4)
								 	json.dump('\nlinear regression test_2 square : %f' % np.sum(test_2 * test_2), outfile, indent = 4)
								