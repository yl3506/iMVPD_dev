import os, json, time, pickle
import nibabel as nib
import numpy as np
from sklearn import linear_model
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### main_out_dir = '/Users/chloe/Documents/output_nondenoise_normalized/'
all_subjects = ['sub-02', 'sub-03']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_nondenoise_normalized/'
### all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rATL', 'rFFA', 'rOFA', 'rSTS']
total_run = 8
regularization_flag = True # if set to fasle, do linear regression

# mask movie data out to a matrix
def batchify(data, mask, shape):
	num_t = shape[3]
	mask_data = np.expand_dims(mask, 3).repeat(num_t, axis=3)
	matrix = (data * mask_data).reshape([num_t, -1])
	return matrix

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
			sub_1_data_dir = work_dir + sub_1 + '_complete/' + sub_1 + '_pre_normalized/' 
			sub_2_data_dir = work_dir + sub_2 + '_complete/' + sub_2 + '_pre_normalized/' 
			if not os.path.exists(out_dir):
				os.makedirs(out_dir)
			
			# iterate through combination of 4 masks
			for mask_1_index in range(0, len(all_masks)):
				for mask_2_index in range(0, len(all_masks)):
					mask_1 = all_masks[mask_1_index]
					mask_2 = all_masks[mask_2_index]
					# initialize data info
					mask_out_dir = out_dir + mask_1 + '_to_' + mask_2 + '/'
					if not os.path.exists(mask_out_dir):
						os.makedirs(mask_out_dir)
					# predict each run iteratively
					for this_run in range(1, total_run + 1): 
						t1 = time.time()
						# load data from this run as testing
						test_1_dir = sub_1_data_dir + sub_1 + '_' + mask_1 + '_run_' + str(this_run) + '_normalized.npy'
						test_2_dir = sub_2_data_dir + sub_2 + '_' + mask_2 + '_run_' + str(this_run) + '_normalized.npy'
						test_1 = np.load(test_1_dir)
						test_2 = np.load(test_2_dir)
						train_1 = []
						train_2 = []
						first_flag = True
						t2 = time.time()
						# load data from all other 7 runs as training
						for run in it.chain(range(1, this_run), range(this_run + 1, total_run + 1)):
							if first_flag:
								train_1 = np.load(sub_1_data_dir + sub_1 + '_' + mask_1 + '_run_' + str(run) + '_normalized.npy')
								train_2 = np.load(sub_2_data_dir + sub_2 + '_' + mask_2 + '_run_' + str(run) + '_normalized.npy')
								first_flag = False
							else:
								train_1 = np.concatenate((train_1, np.load(sub_1_data_dir + sub_1 + '_' + mask_1 + '_run_' + str(run) + '_normalized.npy')))
								train_2 = np.concatenate((train_2, np.load(sub_2_data_dir + sub_2 + '_' + mask_2 + '_run_' + str(run) + '_normalized.npy')))
						
						# fit into model: regularization or linear regression
						if regularization_flag == True: # use regularization model
							# initialize and fit model
							reg = linear_model.MultiTaskElasticNetCV(max_iter=10000, n_jobs=4)
							reg.fit(train_1, train_2)
							t3 = time.time()
							# predict on test set, compute error
							predict_reg = reg.predict(test_1)
							err_reg = predict_reg - test_2
							t4 = time.time()
							# print('regularization squared error: %f' % np.sum(err_reg * err_reg))
							# print('regularization test_2 square: %f' % np.sum(test_2 * test_2))
							# write prediction to file
							out_file = mask_out_dir + 'run_' + str(this_run) + '_regularization_predict.npy'
							np.save(out_file, predict_reg)
							var_ratio = []
							for v in range(0, test_2.shape[1]):
								dif_var = err_reg[:, v].var()
								test_var = test_2[:, v].var()
								if test_var == 0:
									continue
								var_ratio.append(dif_var / test_var)
							var_mean = np.mean(var_ratio)
							out_file_json = mask_out_dir + 'run_' + str(this_run) + '_regularization_predict.json'
							with open(out_file_json, 'w+') as outfile:
								json.dump('mean variance: %f' % var_mean, outfile, indent = 4)
							out_file_coef = mask_out_dir + 'run_' + str(this_run) + '_regularization_pred_coef.npy'
							np.save(out_file_coef, reg.coef_)
							t5 = time.time()
							# print('%f, %f, %f, %f' % (t2 - t1, t3 - t2, t4 - t3, t5 - t4))
						else: # use linear regression model
							# initialize and fit model
							linear = linear_model.LinearRegression()
							linear.fit(train_1, train_2)
							t3 = time.time()					
							# predict on test set, computer error
							predict_lin = linear.predict(test_1)
							err_lin = predict_lin - test_2
							t4 = time.time()
							# print('linear regression squared error: %f' % np.sum(err_lin * err_lin))
							# print('linear regression test_2 square : %f' % np.sum(test_2 * test_2))							
							# write prediction to file
							out_file = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_predict.npy' 
							np.save(out_file, predict_lin)
							var_ratio = []
							for v in range(0, test_2.shape[1]):
								dif_var = err_lin[:, v].var()
								test_var = test_2[:, v].var()
								if test_var == 0:
									continue
								var_ratio.append(dif_var / test_var)
							var_mean = np.mean(var_ratio)
							out_file_json = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_predict.json'
							with open(out_file_json, 'w+') as outfile:
								json.dump('mean variance: %f' % var_mean, outfile, indent = 4)
							out_file_coef = mask_out_dir + 'run_' + str(this_run) + '_linear_reg_pred_coef.npy'
							np.save(out_file_coef, linear.coef_)
							t5 = time.time()
							# print('%f, %f, %f, %f' % (t2 - t1, t3 - t2, t4 - t3, t5 - t4))
