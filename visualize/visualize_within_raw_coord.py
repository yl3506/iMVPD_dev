# visualization of mean variance explained within subject raw on coordinate space
import os
import numpy as np
import matplotlib.pyplot as plt

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3/'
### main_out_dir = '/Users/chloe/Documents/figure_within_raw_pc3/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
total_run = 8
figure_min = 0
figure_max = 0.5
title_y = 1.15
labelpad_x = -300
data = []
out_dir = main_out_dir + 'var_raw_coord.png'

# iterate through all combinations of subjects (including within subject)
for sub_index in range(0, len(all_subjects)):
	
	# initialize info
	subject = all_subjects[sub_index]
	sub_dir = work_dir + subject + '_to_' + subject + '/'
	data_dir = sub_dir + subject + '_to_' + subject + '_raw_ratio_chart.npy'
	if not os.path.exists(main_out_dir):
		os.makedirs(main_out_dir)
	# load data
	cur_data = np.load(data_dir)
	data.append(cur_data.mean())


# plotting
plt.scatter(all_subjects, data)
# additional info in the figure
ax.grid(True)
plt.xlabel('subject')
plt.ylabel('mean var')
plt.title('mean variance explained raw within subject')
plt.savefig(coord_out_dir)
plt.close()