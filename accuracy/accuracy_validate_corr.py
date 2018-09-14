# calculate the correlation of validation data (within MVPD raw and cross MVPD raw)
import os
import numpy as np
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_denoise_pca_1_cross/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3_v3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
data_cross = np.zeros((len(all_masks), len(all_masks))) # initialize overall mean data matrix
data_within = np.zeros((len(all_masks), len(all_masks))) # initialize overall mean data matrix
data_corr = np.zeros((2, len(all_masks) * (len(all_masks) - 1)))
count = 0

# load cross data
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in it.chain(range(0, sub_1_index), range(sub_1_index + 1, len(all_subjects))):
		# initialize info
		sub_1 = all_subjects[sub_1_index]
		sub_2 = all_subjects[sub_2_index]
		sub_dir = work_dir + sub_1 + '_to_' + sub_2 + '/'
		data_dir = sub_dir + sub_1 + '_to_' + sub_2 + '_raw_ratio_chart.npy'
		# load data
		data_cross += np.load(data_dir)
		count += 1
# calculate mean of all matrices
data_cross = data_cross / count
# erase diagonal
data_cross[range(len(all_masks)), range(len(all_masks))] = np.nan
# remove nan
data_corr[0, :] = np.squeeze(np.concatenate((np.delete(data_cross[0, :], 0), np.delete(data_cross[1, :], 1), 
		np.delete(data_cross[2, :], 2), np.delete(data_cross[3, :], 3), np.delete(data_cross[4, :], 4), 
		np.delete(data_cross[5, :], 5), np.delete(data_cross[6, :], 6))))


# load within data
count = 0
for sub_index in range(0, len(all_subjects)):
	# initialize info
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	data_dir = sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy'
	# load data
	data_within += np.load(data_dir)
	count += 1
# calculate mean of all matrices
data_within = data_within / count
# erase diagonal
data_within[range(len(all_masks)), range(len(all_masks))] = np.nan
# remove nan
data_corr[1, :] = np.squeeze(np.concatenate((np.delete(data_within[0, :], 0), np.delete(data_within[1, :], 1), 
		np.delete(data_within[2, :], 2), np.delete(data_within[3, :], 3), np.delete(data_within[4, :], 4), 
		np.delete(data_within[5, :], 5), np.delete(data_within[6, :], 6))))


# calculate correlation
corr = np.corrcoef(data_corr)
print(corr)


