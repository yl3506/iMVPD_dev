# visualize same region prediction comparison between within subject and cross subject (raw var)
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3_local/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/output_cos_compcorr_pc3_v3/'
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'same_region_pc3_v3.png'
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
within_list = []
cross_list = []
ind = np.arange(len(all_masks))  # the x locations for the groups
width = 0.3 # the width of the bars
first_ind = 0.16258

# iterate through all rois to append list
for roi_index in range(0, len(all_masks)):
	within_dir = work_dir + all_masks[roi_index] + '_overall_var_within.txt'
	within_list.append(float(np.loadtxt(within_dir)))
	cross_dir = work_dir + all_masks[roi_index] + '_overall_var_cross.txt'
	cross_list.append(float(np.loadtxt(cross_dir)))

# plotting
fig = plt.figure()
ax = fig.add_subplot(111)
yvals = within_list
rects1 = ax.bar(ind+first_ind, yvals, width, color='green')
zvals = cross_list
rects2 = ax.bar(first_ind+ind+width, zvals, width, color='orange')

ax.set_ylabel('variance explained raw')
ax.set_xticks(first_ind + ind + width)
ax.set_xticklabels(all_masks)
ax.legend( (rects1[0], rects2[0]), ('within', 'cross'))
plt.title('compare same roi prediction of within and cross sub, pc=3') # set title

# save figure
plt.savefig(out_dir)