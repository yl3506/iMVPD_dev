import os, time, json
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### main_dir = '/Users/chloe/Documents'
### all_subjects = ['sub-02', 'sub-04']
main_dir = '/mindhive/saxelab3/anzellotti/forrest/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
color_list = ['red', 'fuchsia', 'orange', 'yellow', 'green', 'teal', 'cyan', 'blue', 'purple', 'brown', 'grey']
pc_num = 2 # number of principal component used
first_flag = True
data = []
figure_max = 0.4
figure_min = 0
title_y = 1.15 # title distance to the top margin
labelpad_x = -300

# load data
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in range(0, len(all_subjects)):
		# iniialize data info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		data_dir = work_dir + sub_1 + '_to_' + sub_2 + '/' + sub_1 + '_to_' + sub_2 + '_vector.npy'
		data_temp = np.load(data_dir)
		# load data
		if first_flag:
			data = data_temp.T # 1 x r
			first_flag = False
		else:
			data = np.concatenate((data, data_temp.T))# s x r

# do pca 
pca = PCA(n_components=pc_num)
pca.fit(data)
data_pc = pca.transform(data) # s x 2
weight = pca.components_ # 2 x r

# visualize pc coordinates
x = data_pc[:, 0]
y = data_pc[:, 1]
x_list = [] # list of predictors subject
y_list = []
fig, ax = plt.subplots() # initialize plot
# color predictor subject seperately
cur_index = 0
for sub_index in range(0, len(all_subjects)):
	x_list.append(x[cur_index: cur_index + len(all_subjects)])
	y_list.append(y[cur_index: cur_index + len(all_subjects)])
	cur_index += len(all_subjects)
	# plot
	ax.scatter(x_list[sub_index], y_list[sub_index], c=color_list[sub_index], label=all_subjects[sub_index])
# additional info in the figure
ax.legend(loc = 6)
ax.grid(True)
plt.xlabel('first component')
plt.ylabel('second component')
plt.title('2 component coordinates for all subject pairs')
coord_out_dir = main_dir + 'pc_coordinates_colored.png'
plt.savefig(coord_out_dir)
plt.close()

# visualize pc weight matrices
weight_1 = weight[0, :].reshape(len(all_masks), len(all_masks))
weight_1_out_dir = main_dir + 'weight_1_matrix.png'
plt.matshow(weight_1, vmin=-0.3, vmax=0, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor') # set y axis label
plt.title('first component weight, pc=3', y=title_y) # set title
plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
plt.savefig(weight_1_out_dir) # save figure
plt.close()
# second weight matrix
weight_2 = weight[1, :].reshape(len(all_masks), len(all_masks))
weight_2_out_dir = main_dir + 'weight_2_matrix.png'
plt.matshow(weight_2, vmin=-0.2, vmax=0.3, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.ylabel('Predictor') # set y axis label
plt.title('second component weight, pc=3', y=title_y) # set title
plt.xlabel('Target', labelpad=labelpad_x) # set x axis label
plt.savefig(weight_2_out_dir) # save figure
plt.close()
