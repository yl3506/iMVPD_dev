## filter out confound xyz (and rotate) data and save in seperate directory
import os, csv
import numpy as np
import scipy as sp

# initalize data
work_dir = '/mindhive/saxelab3/anzellotti/forrest/derivatives/fmriprep/'
all_subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-09', 'sub-10', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
### work_dir = '/Users/chloe/Documents/'
### all_subjects = ['sub-02', 'sub-04']
total_run = 8
start_index = 0 # starting column number of xyz data
end_index = 0 # ending column number of xyz data

# iterate through all subjects
for sub in all_subjects:
	
	# initialize data
	sub_dir = work_dir + sub + '_complete/'
	sub_out_dir = sub_dir + sub + '_xyz/'
	if not os.path.exists(sub_out_dir):
		os.makedirs(sub_out_dir)
	
	# load the data from all runs
	for run in range(1, total_run + 1):		
		# read in cosine data
		data_dir = sub_dir + 'ses-movie/func/' + sub + '_ses-movie_task-movie_run-' + str(run) + '_bold_confounds.tsv'
		data = sp.genfromtxt(data_dir, delimiter="\t")
		# get the header info
		header = []
		with open(data_dir) as fd:
			rd = csv.reader(fd, delimiter="\t")
			for row in rd:
				header = row
				break # get the first row of file
		header_len = len(header)
		print(header_len)
		end_index = header_len
		start_index = end_index - 6
		# save cosine data to file
		xyz_data = data[1:, start_index:end_index] # first row is label
		out_file = sub_out_dir + sub + '_run_' + str(run) + '_xyz.npy'
		np.save(out_file, xyz_data)