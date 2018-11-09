# calculate correlation of subjects by within-MVPD raw var, and do PCA/ICA
# subject x region pair matrix as input, namely, [11, 49]
import os, time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from sklearn.linear_model import LinearRegression

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

# apply pca/ica
pca = FastICA(n_components=num_pc)
pca.fit(data) # [11, 49] -> [11, 2], data X
data_pc = pca.transform(data) # [11, 2] E
#print(pca.components_)
components = pca.components_ # component weights [2, 49]

# now we want to find how much variance these 2 components explained
X = data # [11,49], 11 subjects, 49 region pairs
E = components # [2,49], 2 components, 49 region pairs as features
# XX, [11,49], the approximated result of linear combination of components
XX = np.zeros_like(X)
for i in range(len(all_subjects)): # iterate through each subject vector [1,49]
	# approximate current subject vector [1,49] as a linear combination of 2 components [2,49]
	lreg = LinearRegression().fit(E.T, X[i,:].T) 
	# E.T:[n_samples(49), n_features(2)], X[i,:].T: [n_samples(49), n_target(1)]
	XX[i,:] = lreg.predict(E.T).T 
	# input E.T:[n_samples(49),n_features(2)], output:[n_samples(49), n_target(1)], XX[i,:]=output.T
# now project the orginal data X[11,49], 
# and the linear combination approximation XX[11,49] onto the same PCA space
pca2 = PCA()
# pad X for sklearn implementation
X_mean = X.mean(0) # [1, 49]
X = np.concatenate((X, np.tile(X_mean, X.shape[1]-X.shape[0]))) # [49,49]
pca2.fit(X) # [11, 49] = [n_samples, n_features], max will have 11 components
# X2 is the projection of original data X onto the PCA space
X2 = pca2.transform(X) # output X2:[11,11] = [n_samples, n_components]
# XX2 is the projection of the approximated data XX onto the same PCA space
XX2 = pca2.transform(XX) # output XX2: [11,11] = [n_samples, n_components]
# now we calculate the varexp for each column (feature/region-pair)
var = np.zeros((1,len(all_subjects))) # [1,11] varexp for each column
for i in range(len(all_subjects)):
	# varexp for each column/dimension/region-pair
	var[0,i] = 1 - np.var(X2[:,i] - XX2[:,i]) / np.var(X2[:,i])
# now we calculate the total varexp of the original data explained by the 2 components together
total_var = 0
for i in range(len(all_subjects)): # iterate through each column
	# collect the varexp for each dimension/feature/region-pair
	total_var += pca.explained_variance_ratio_[i] * var[0,i]
# print total varexp of the original data explained by the 2 components together
print(total_var)

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
if component1.mean() < 0: # flip sign for better visualization
	component1 = component1 * (-1)
if component2.mean() < 0:
	component2 = component2 * (-1)
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

