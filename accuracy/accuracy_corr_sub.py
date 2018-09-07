# calculate correlation of subjects by within-MVPD raw var
import os, time
import numpy as np

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### all_subjects = ['sub-02', 'sub-05']
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_global_compcorr_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
data = np.zeros((len(all_subjects), len(all_masks) * len(all_masks)))
out_dir = work_dir + 'corr_sub_within.npy'

# iterate through all subjects
for sub_index in range(0, len(all_subjects)):
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	sub_data = np.load(sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy')
	data[sub_index, :] = np.squeeze(sub_data.reshape((1, -1)))

# calculate correlation
corr = np.corrcoef(data)
# save correlation to file
np.save(out_dir, corr)
