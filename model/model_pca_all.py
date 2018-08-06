## main model for ROI prediction
import os, time, json
import numpy as np
from sklearn import linear_model
import itertools as it
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d

# initialize parameters
### work_dir = '/Users/chloe/Documents/'
### main_out_dir = '/Users/chloe/Documents/output_cos_pc3_v2/'
### all_subjects = ['sub-18', 'sub-20']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
regularization_flag = False # if set to false, do linear regression
pc_num = 3 # number of principal component used
smooth_flag = False # whether to smooth data before modeling
sigma = 2 # standard deviation for Gaussian kernel

# iterate through all combinations of subjects (including within subject)
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# iniialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		out_dir = main_out_dir + sub_1 + '_to_' + sub_2 + '/'
		sub_1_data_dir = work_dir + sub_1 + '_complete/' + sub_1 + '_decosed_normalized_demean/' 
		sub_2_data_dir = work_dir + sub_2 + '_complete/' + sub_2 + '_decosed_normalized_demean/' 
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		# iterate through all combinations of mask
		for mask_1_index in range(0, len(all_masks)):
			for mask_2_index in range(0, len(all_masks)):
				# initialize data info
				mask_1 = all_masks[mask_1_index]
				mask_2 = all_masks[mask_2_index]
				mask_out_dir = out_dir + mask_1 + '_to_' + mask_2 + '/'
				if not os.path.exists(mask_out_dir):
					os.makedirs(mask_out_dir)
				# predict each run iteratively
				for this_run in range(1, total_run + 1):
					# load data from this run as testing
					test_1_dir = sub_1_data_dir + sub_1 + '_' + mask_1 + '_run_' + str(this_run) + '_decosed_normalized.npy'
					test_2_dir = sub_2_data_dir + sub_2 + '_' + mask_2 + '_run_' + str(this_run) + '_decosed_normalized.npy'
					test_1 = np.load(test_1_dir) # t x v
					test_2 = np.load(test_2_dir)
					train_1 = [] # 7t x v
					train_2 = []
					first_flag = True
					t2 = time.time()
					# load data from all other 7 runs as training
					for run in it.chain(range(1, this_run), range(this_run + 1, total_run + 1)):
						if first_flag:
							train_1 = np.load(sub_1_data_dir + sub_1 + '_' + mask_1 + '_run_' + str(run) + '_decosed_normalized.npy')
							train_2 = np.load(sub_2_data_dir + sub_2 + '_' + mask_2 + '_run_' + str(run) + '_decosed_normalized.npy')
							first_flag = False
						else:
							train_1 = np.concatenate((train_1, np.load(sub_1_data_dir + sub_1 + '_' + mask_1 + '_run_' + str(run) + '_decosed_normalized.npy')))
							train_2 = np.concatenate((train_2, np.load(sub_2_data_dir + sub_2 + '_' + mask_2 + '_run_' + str(run) + '_decosed_normalized.npy')))
					# do pca for training and testing data
					pca_train_1 = PCA(n_components=pc_num)
					pca_train_2 = PCA(n_components=pc_num)
					pca_train_1.fit(train_1)
					pca_train_2.fit(train_2)
					train_1_pc = pca_train_1.transform(train_1) # 7t x pc_num
					train_2_pc = pca_train_2.transform(train_2)
					test_1_pc = pca_train_1.transform(test_1) # t x pc_num
					test_2_pc = pca_train_2.transform(test_2)
					# smooth data
					if smooth_flag:
						train_1_pc = gaussian_filter1d(train_1_pc.T, sigma).T
						train_2_pc = gaussian_filter1d(train_2_pc.T, sigma).T
						test_1_pc = gaussian_filter1d(test_1_pc.T, sigma).T
						test_2_pc = gaussian_filter1d(test_2_pc.T, sigma).T
					# save explained variance ratio
					train_1_var_ratio = pca_train_1.explained_variance_ratio_ 
					train_2_var_ratio = pca_train_2.explained_variance_ratio_ # 1 x pc_num
					train_2_var = pca_train_2.explained_variance_ # 1 x pc_num
					# fit into model: regularization or linear regression
					if regularization_flag == True: # use regularization model
						# initialize and fit model
						reg = linear_model.MultiTaskElasticNetCV(max_iter=10000, n_jobs=4, alphas=[0.01])
						reg.fit(train_1_pc, train_2_pc)
						# predict on test set, compute error
						predict_reg = reg.predict(test_1_pc)
						err_reg = predict_reg - test_2_pc
						# save prediction
						out_file = mask_out_dir + 'run_' + str(this_run) + '_regularization_predict_001.npy'
						np.save(out_file, predict_reg)
						# save variance ratio and penalization
						var_ratio = err_reg.var() / test_2_pc.var()
						out_file_json = mask_out_dir + 'run_' + str(this_run) + '_regularization_predict_001.json'
						with open(out_file_json, 'w+') as outfile:
							json.dump('variance ratio (err_var / ans_var): %f' % var_ratio + ', alpha chosen: %f' % reg.alpha_, outfile, indent = 4)
						# save coefficients
						out_file_coef = mask_out_dir + 'run_' + str(this_run) + '_regularization_pred_coef_001.npy'
						np.save(out_file_coef, reg.coef_)
						# save smoothed answer
						out_file_ans = mask_out_dir + 'run_' + str(this_run) + '_regularization_answer_001.npy'
						np.save(out_file_ans, test_2_pc)

					else: # use linear regression model
						# initialize and fit model
						linear = linear_model.LinearRegression()
						linear.fit(train_1_pc, train_2_pc)
						# predict on test set, computer error
						predict_lin = linear.predict(test_1_pc)
						err_lin = predict_lin - test_2_pc
						# save prediction
						out_file = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_predict.npy'
						np.save(out_file, predict_lin)

						# save variance ratio and penalization
						# var_ratio = 0
						# for v in range(0, err_lin.shape[1]):
						# 	var_ratio += (1 - (err_lin[:, v].var() / test_2_pc[:,v].var())) * (train_2_var[v] / train_2_var.sum())
						# if var_ratio < 0:
						# 	var_ratio = 0


						# calculate the component variance explained
						V1 = pca_train_2 # from normal to 3 pc, answer
						V2 = PCA() # from normal to normal
						V2.fit(test_2) 
						# variance to total components on V2
						test_2_on_v2 = V2.transform(test_2) # projection of test_2 on V2
						pred_on_v2 = V2.transform(V1.inverse_transform(predict_lin)) # projection of prediction on V2
						err_on_v2 = test_2_on_v2 - pred_on_v2 # t x v
						v2_var_ratio = V2.explained_variance_ratio_
						v2_var = 0
						for v in range(0, test_2_on_v2.shape[1]):
							v2_var += (1 - (err_on_v2[:, v].var() / test_2_on_v2[:, v].var())) * v2_var_ratio[v]
						# variance to 3 pc on V2
						test_2_on_v1_to_v2 = V2.transform(V1.inverse_transform(V1.transform(test_2)))
						err_v1_v2 = test_2_on_v2 - test_2_on_v1_to_v2
						v1_v2_var = 0
						for v in range(0, test_2_on_v1_to_v2.shape[1]):
							v1_v2_var += (1 - (err_v1_v2[:, v].var() / test_2_on_v2[:, v].var())) * v2_var_ratio[v]
						# final variance
						var_ratio = v2_var / v1_v2_var # variance to 3 pcs on V2 with respect to V1
						if var_ratio < 0:
							var_ratio = 0
						if v2_var < 0:
							v2_var = 0
						# save variance to file
						out_file_txt_3pc = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_ratio_pc3.txt'
						with open(out_file_txt_3pc, 'w+') as outfile:
							outfile.write(str(var_ratio)) # variance explained
						out_file_txt_tot = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_ratio_total.txt'
						with open(out_file_txt_tot, 'w+') as outfile:
							outfile.write(str(v2_var)) # variance explained
						

						# save coefficients
						out_file_coef = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_pred_coef.npy'
						np.save(out_file_coef, linear.coef_)
						
						# save smoothed answer
						out_file_ans = mask_out_dir + 'run_' + str(this_run) + '_linear_regression_answer.npy'
						np.save(out_file_ans, test_2_pc)
