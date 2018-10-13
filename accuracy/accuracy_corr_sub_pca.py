# calculate correlation of subjects by within-MVPD raw var, and do PCA/ICA
import os, time
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
main_dir = '/mindhive/saxelab3/anzellotti/forrest/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_global_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
num_pc = 2
coord_out_dir = main_dir + 'corr_sub_within_ICA.png'
component1_dir = main_dir + 'sub_ica_component1.png'
component2_dir = main_dir + 'sub_ica_component2.png'
title_y = 1.15

# get data
data = np.zeros((len(all_subjects), len(all_masks) * len(all_masks))) # [11, 49]
for sub_index in range(0, len(all_subjects)):
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	sub_data = np.load(sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy')
	data[sub_index, :] = np.squeeze(sub_data.reshape((1, -1)))

# apply pca
pca = FastICA(n_components=num_pc)
pca.fit(data) # [11, 49] -> [11, 2]
data_pc = pca.transform(data) # [11, 2]
print(pca.components_)
components = pca.components_

# visualize the projection on pc coordinate
fig, ax = plt.subplots() # initialize plot
ax.scatter(data_pc[:, 0], data_pc[:, 1], c='green')
# additional info in the figure
ax.grid(True)
plt.xlabel('first component')
plt.ylabel('second component')
plt.title('corr ICA for all subjects, glb+cpcr')
plt.savefig(coord_out_dir)
plt.close()

# plot component weights
component1 = np.squeeze(components[0,:].reshape((7,7)))
component2 = np.squeeze(components[1,:].reshape((7,7)))
# generate figure
plt.matshow(component1, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.title('1st component weight, sub x region, glb+cpcr', y=title_y) # set title
plt.savefig(component1_dir) # save figure
plt.close()
# second component figure
plt.matshow(component2, cmap='jet') # plot matrix
plt.xticks(np.arange(len(all_masks)), all_masks) # set x axis tick
plt.yticks(np.arange(len(all_masks)).T, all_masks) # set y axis tick
plt.colorbar() # show color bar
plt.title('2nd component weight, sub x region, glb+cpcr', y=title_y) # set title
plt.savefig(component2_dir) # save figure
plt.close()

