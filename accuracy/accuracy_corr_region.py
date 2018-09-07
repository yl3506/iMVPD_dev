# calculate correlation of region pairs by within-MVPD raw var, and do PCA
import os, time
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
main_dir = '/mindhive/saxelab3/anzellotti/forrest/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_global_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
num_pc = 2
data_out_dir = work_dir + 'corr_region_within.npy'
# corr_out_dir = main_dir + 'corr_region_within.png'
coord_out_dir = main_dir + 'corr_region_within_pca.png'

# get data
data = np.zeros((len(all_subjects), len(all_masks) * len(all_masks))) # [11, 49]
for sub_index in range(0, len(all_subjects)):
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	sub_data = np.load(sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy')
	data[sub_index, :] = np.squeeze(sub_data.reshape((1, -1)))

# calculate correlation
corr = np.corrcoef(data.T) # [49, 49] <- [49, 11]
# save correlation to file
np.save(data_out_dir, corr)

# visualize the correlation?

# apply pca
pca = PCA(n_components=num_pc)
pca.fit(data.T) # [49, 11]
data_pc = pca.transform(data.T) # [49, 2]

# visualize the projection on pc coordinate
fig, ax = plt.subplots() # initialize plot
face = []
scene = []
between = []
# color networks seperately
for index in [0, 1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17, 21, 22, 23, 24]: # face
	face.append(data_pc[index, :])
face = np.array(face)
ax.scatter(face[:, 0], face[:, 1], c='pink', label='face')
for index in [32, 33, 34, 39, 40, 41, 46, 47, 48]: # scene
	scene.append(data_pc[index, :])
scene = np.array(scene)
ax.scatter(scene[:, 0], scene[:, 1], c='green', label='scene')
for index in [4, 5, 6, 11, 12, 13, 18, 19, 20, 25, 26, 27, 28, 29, 30, 31, 35, 36, 37, 38, 42, 43, 44, 45]: # between network
	between.append(data_pc[index, :])
between = np.array(between)
ax.scatter(between[:, 0], between[:, 1], c='blue', label='between')
# additional info in the figure
ax.legend(loc=2)
ax.grid(True)
plt.xlabel('first component')
plt.ylabel('second component')
plt.title('2 pc coordinates for all region pairs, glb+cpcr')
plt.savefig(coord_out_dir)
plt.close()
