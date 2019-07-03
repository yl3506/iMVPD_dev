import numpy as np
import itertools as it
import random, sys
import scipy.stats as stats

data_dir1 = '/Users/chloe/Documents/Yichen/output_compcorr_pc3_v3/'
data_dir2 = '/Users/chloe/Documents/Yichen/output_nondenoise_pc3_v3/'
all_subjects = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-09', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
all_masks = ['rOFA', 'rFFA', 'rATL', 'rSTS', 'rTOS', 'rPPA', 'rPC']
num_sets = 10

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
'''
print('----------------- Two independent sample t-test ------------------')

# bootstrapping for std and mean
mean1 = []
mean2 = []
var1 = []
var2 = []
def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

# Pick several sets of 5 non-overlapping pairs of participants
for i in range(0, num_sets):
	values1 = []
	values2 = []
	# pick 5 pairs from data1
	sublist = all_subjects.copy()
	while len(sublist)>=3:
	    rand1 = pop_random(sublist)
	    rand2 = pop_random(sublist)
	    value1 = data_within1 - np.mean(np.load(data_dir1+rand1+'_to_'+rand2+'/'\
	    	+rand1+'_to_'+rand2+'_raw_ratio_chart.npy'))
	    values1.append(value1)
	# pick 5 pairs from data2
	sublist = all_subjects.copy()
	while len(sublist)>=3:
	    rand1 = pop_random(sublist)
	    rand2 = pop_random(sublist)
	    value2 = data_within2 - np.mean(np.load(data_dir2+rand1+'_to_'+rand2+'/'\
	    	+rand1+'_to_'+rand2+'_raw_ratio_chart.npy'))
	    values2.append(value2)
	# Calculate mean and std deviation for this 5-pairs
	mean1.append(np.mean(values1))
	mean2.append(np.mean(values2))
	var1.append(np.var(values1))
	var2.append(np.var(values2))
# Average the means and std deviations for all sets
mean1 = np.mean(mean1)
mean2 = np.mean(mean2)
var1 = np.mean(var1)
var2 = np.mean(var2)
print('mean1 = %f, mean2 = %f, var1 = %f, var2 = %f' % (mean1, mean2, var1, var2))

# pooled variances test for equal sample sizes 
n = len(all_subjects)*(len(all_subjects) - 1)
t = ((mean1 - mean2) - 0) / np.sqrt((var1+var2)/n)
pval = stats.t.sf(np.abs(t), n+n-2)*2  # two-sided pvalue = Prob(abs(t)>t)
print('t = %f' % t)
print('pval =', pval)


'''
Matched t-test:
For each of the 11x10 pairs, 
calculate difference of two denoising methods: 
delta_varexp nondenoise - delta_varexp compcorr
'''
print('----------------------- Matched t-test ----------------------')
diff = []
for sub_1_index in range(0, len(all_subjects)):
	for sub_2_index in it.chain(range(0, sub_1_index), range(sub_1_index + 1, len(all_subjects))):
		data1 = np.mean(np.load(data_dir1+all_subjects[sub_1_index]+'_to_'+all_subjects[sub_2_index]+'/'\
							+all_subjects[sub_1_index]+'_to_'+all_subjects[sub_2_index]+'_raw_ratio_chart.npy'))
		data2 = np.mean(np.load(data_dir2+all_subjects[sub_1_index]+'_to_'+all_subjects[sub_2_index]+'/'\
							+all_subjects[sub_1_index]+'_to_'+all_subjects[sub_2_index]+'_raw_ratio_chart.npy'))
		diff.append((data_within1 - data1) - (data_within2 - data2))
sd = np.sqrt(1/(n-1) * (np.sum(np.multiply(diff,diff))-(np.sum(diff))**2/n)) # standard deviation of diff
t = np.mean(diff) / (sd/np.sqrt(n))
pval = stats.t.sf(np.abs(t), n-1)*2  # two-sided pvalue = Prob(abs(t)>t)
print('t = %f' % t)
print('pval =', pval)
















