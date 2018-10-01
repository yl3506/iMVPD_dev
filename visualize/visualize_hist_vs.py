# visualize the histogram of mean vs result
import os
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
from matplotlib.ticker import MaxNLocator

# initialize parameters
### work_dir = '/Users/chloe/Documents/output_cos_compcorr_pc3_local/'
### main_out_dir = '/Users/chloe/Documents/'
work_dir = '/mindhive/saxelab3/anzellotti/forrest/'
all_denoise = ['nodenoise', 'global', 'cos', 'xyz', 'compcorr']
data_dir = ['output_nondenoise_pc3_v3/', 'output_global_pc3_v3/', 'output_cos_pc3_v3/', 'output_xyz_pc3_v3/', 'output_compcorr_pc3_v3/']
main_out_dir = '/mindhive/saxelab3/anzellotti/forrest/'
out_dir = main_out_dir + 'vs_hist.png'
data_list = []
ind = np.arange(len(data_dir))  # the x locations for the groups
width = 0.5 # the width of the bars
first_ind = 0.16258

# iterate through all rois to append list
for index in range(0, len(all_denoise)):
	cur_data_dir = work_dir + data_dir[index] + 'vs_' + all_denoise[index] + '_pc3_v3.npy'
	cur_data = np.load(cur_data_dir)
	cur_data = np.concatenate((np.delete(cur_data[0, :], 0), np.delete(cur_data[1, :], 1), 
		np.delete(cur_data[2, :], 2), np.delete(cur_data[3, :], 3), np.delete(cur_data[4, :], 4), 
		np.delete(cur_data[5, :], 5), np.delete(cur_data[6, :], 6)))
	cur_data = cur_data.mean()
	data_list.append(cur_data)

# plotting
# fig = plt.hist(data_list, all_denoise,rwidth=0.8, color='green')
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Denoising Methods')
# plt.ylabel('Mean var difference (within-cross)')
# plt.title('Mean Var Difference for Single Denoising')
# pltsavefig(out_dir)

fig = plt.figure()
ax = fig.add_subplot(111)
yvals = data_list
rect = ax.bar(ind + first_ind, yvals, width, color='green')

# ax.set_ylabel('Mean var difference (within-cross)')
ax.set_xticks(first_ind + ind + width * 0.5)
ax.set_xticklabels(all_denoise)
for tick in ax.xaxis.get_major_ticks():
	tick.label.set_fontsize(20)
plt.xticks(rotation=11)
#plt.locator_params(axis='y', nbins=6) # reduce number of yticks
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.grid(axis = 'y', alpha = 0.8)
# plt.title('Mean Var Difference for Single Denoising') # set title

# save figure
plt.savefig(out_dir)