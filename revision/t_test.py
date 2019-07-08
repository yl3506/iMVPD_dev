# need to run with python3
import numpy as np
import itertools as it
import random, sys
import scipy.stats as stats

data_dir1 = '/Users/chloe/Documents/Yichen/output_global_compcorr_pc3_v3/'
data_dir2 = '/Users/chloe/Documents/Yichen/output_nondenoise_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
num_sets = 100 # number of iteration for bootstrapping

print(data_dir1)

# get means of within varexp
data_within1 = 0
data_within2 = 0
for sub_index in range(0, len(all_subjects)):
	subject = all_subjects[sub_index]
	sub_dir1 = data_dir1 + subject + '_to_' + subject + '/'
	data_within_dir1 = sub_dir1 + subject + '_to_' + subject + '_raw_ratio_chart.npy'
	data_within1 += np.mean(np.load(data_within_dir1))
	sub_dir2 = data_dir2 + subject + '_to_' + subject + '/'
	data_within_dir2 = sub_dir2 + subject + '_to_' + subject + '_raw_ratio_chart.npy'
	data_within2 += np.mean(np.load(data_within_dir2))
data_within1 = data_within1 / len(all_subjects)
data_within2 = data_within2 / len(all_subjects)

'''
Two independent sample t-test
delta_varexp compcorr - delta_varexp nodenoise
'''
print('----------------- Matched t-test ------------------')

# bootstrapping for std and mean
meanD = [] # mean of difference
stdD = [] # std of difference
std1 = [] # seperately calculate std for data 1
def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

# Pick several sets/iterations of 5 non-overlapping pairs of participants
for i in range(0, num_sets):
	values1 = []
	values2 = []
	# pick 5 pairs from data1
	sublist = all_subjects.copy()
	while len(sublist)>=3:
	    rand1 = pop_random(sublist)
	    rand2 = pop_random(sublist)
	    value1 = np.mean(np.load(data_dir1+rand1+'_to_'+rand1+'/'+\
	    		rand1+'_to_'+rand1+'_raw_ratio_chart.npy') - \
	    		np.load(data_dir1+rand1+'_to_'+rand2+'/'\
	    		+rand1+'_to_'+rand2+'_raw_ratio_chart.npy')) # within-cross
	    values1.append(value1)
		# apply the same 5 pairs to the second data folder
	    value2 = np.mean(np.load(data_dir2+rand1+'_to_'+rand1+'/'+\
	    		rand1+'_to_'+rand1+'_raw_ratio_chart.npy') - \
	    		np.load(data_dir2+rand1+'_to_'+rand2+'/'\
	    		+rand1+'_to_'+rand2+'_raw_ratio_chart.npy')) # within-cross
	    values2.append(value2)
	# Calculate mean and std deviation for this 5-pairs
	meanD.append(np.mean(np.array(values1) - np.array(values2)))
	stdD.append(np.std(np.array(values1) - np.array(values2), ddof=1))
	std1.append(np.std(values1, ddof=1))
# Average the means and std deviations for all iterations of bootstrapping
meanD = np.mean(meanD)
stdD = np.mean(stdD)
std1 = np.mean(std1)
print('std1 = %f' % std1)
print('meanD = %f, stdD = %f' % (meanD, stdD))

# direct difference method
print('----- DF=4 -----')
n = 5
t = meanD / (stdD / np.sqrt(n))
df = 4
pval = stats.t.sf(np.abs(t), df)*2  # two-sided pvalue = Prob(abs(t)>t)
print('t = %f' % t)
print('Df=4, pval =', pval)

print('----- DF=10 -----')
# direct difference method
n = 5
t = meanD / (stdD / np.sqrt(n))
df = 10
pval = stats.t.sf(np.abs(t), df)*2  # two-sided pvalue = Prob(abs(t)>t)
print('t = %f' % t)
print('Df=10, pval =', pval)















