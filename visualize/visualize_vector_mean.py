# visualize the chart of all subject vector mean
# visualize the chart of all subject vector mean removing half row and vector mean
# visualize the chart of all subject vector network-wise mean
import os, time
import numpy as np
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_subjects_num = ['01', '02', '04', '05', '09', '15', '16', '17', '18', '19', '20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
matrix_out_dir = main_out_dir + 'sub_vector_matrix.png'
matrix_new_out_dir = main_out_dir + 'sub_vector_matrix_demean.png'
matrix_net1_out_dir = main_out_dir + 'sub_vector_matrix_net1.png'
matrix_net2_out_dir = main_out_dir + 'sub_vector_matrix_net2.png'
net1_num = 4 # number of rois in network 1 (face network)
title_y = 1.15 # title distance to the top margin
labelpad_x = -300
matrix = np.zeros((len(all_subjects), len(all_subjects))) # initialize overall mean data matrix
matrix_new = np.zeros((len(all_subjects), len(all_subjects))) 
matrix_net1 = np.zeros((len(all_subjects), len(all_subjects)))
matrix_net2 = np.zeros((len(all_subjects), len(all_subjects))) 


# visualize the chart of all subject vector mean
# fill in matrix values
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# initialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_vector.npy'
		data = np.load(data_dir)
		mean = data.mean()
		matrix[sub_1_index, sub_2_index] = mean
# generate figure
plt.matshow(matrix, vmin=0, vmax=0.05, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_subjects)), all_subjects_num) # set x axis tick
plt.yticks(np.arange(len(all_subjects)).T, all_subjects_num) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor subject') # set y axis label
plt.title('mean var explained raw of all regions, pc=3', y=title_y) # set title
plt.xlabel('Target subject', labelpad=labelpad_x) # set x axis label
plt.savefig(matrix_out_dir) # save figure
plt.close()


# visualize the chart of all subject vector mean removing half row and vector mean
row_mean = matrix.mean(axis = 1, keepdims = False) # mean of each row, s x 1
column_mean = matrix.mean(axis = 0, keepdims = True) # mean of each column, 1 x s
# remove half mean
matrix_new = matrix - (1/2) * row_mean - (1/2) * column_mean
# generate figure
plt.matshow(matrix_new, vmin=-0.015, vmax=0.007, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_subjects)), all_subjects_num) # set x axis tick
plt.yticks(np.arange(len(all_subjects)).T, all_subjects_num) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor subject') # set y axis label
plt.title('mean var explained raw of all regions demean, pc=3', y=title_y) # set title
plt.xlabel('Target subject', labelpad=labelpad_x) # set x axis label
plt.savefig(matrix_new_out_dir) # save figure
plt.close()


# visualize the chart of all subject vector network-wise mean
# fill in matrices values
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# initialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_raw_ratio_chart.npy' # r x 1
		data = np.load(data_dir)
		# split vectors into network 1 (face regions) data and network 2 (scene regions) data
		data_net1 = data[:net1_num, :net1_num]
		data_net2 = data[net1_num:, net1_num:]
		mean_net1 = data_net1.mean()
		mean_net2 = data_net2.mean()
		matrix_net1[sub_1_index, sub_2_index] = mean_net1
		matrix_net2[sub_1_index, sub_2_index] = mean_net2
# generate figure
plt.matshow(matrix_net1, vmin=0, vmax=0.05, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_subjects)), all_subjects_num) # set x axis tick
plt.yticks(np.arange(len(all_subjects)).T, all_subjects_num) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor subject') # set y axis label
plt.title('mean var explained raw of face network, pc=3', y=title_y) # set title
plt.xlabel('Target subject', labelpad=labelpad_x) # set x axis label
plt.savefig(matrix_net1_out_dir) # save figure
plt.close()
# generate figure
plt.matshow(matrix_net2, vmin=0, vmax=0.05, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_subjects)), all_subjects_num) # set x axis tick
plt.yticks(np.arange(len(all_subjects)).T, all_subjects_num) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor subject') # set y axis label
plt.title('mean var explained raw of scene network, pc=3', y=title_y) # set title
plt.xlabel('Target subject', labelpad=labelpad_x) # set x axis label
plt.savefig(matrix_net2_out_dir) # save figure
plt.close()


		