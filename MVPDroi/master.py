### main execution function
import os

## environment and input setup
# import necessary libraries and variables
# specify the input, and parameters
data_directory = '/Users/chloe/Documents/data_test/'
num_subject = 2 # total number of subjects
all_sub_list = [] # list of all subjects
[0.01, 0.03, 0.1, 0.3, 1.0, 3.0]

# iterate through subject combinations and load model
os.chdir(data_directory)
all_data_files = os.listdir() # list all files in current
for data_file in all_data_files: 
	# filter to select subject folders only
	if 'sub-' in data_file:
		all_sub_list.append(data_file)


## preprocessing and region models
# processing model, reduce noise
# save the result to new input folders


## seperate the dataset by 3 parts
## set ouput folders

## regularization
# fix lambda
# determine which pair to train
# train with part A to find the prediction function


## validation and performance
# test the prediction function with part B to find error performnace
# save the performance into a list


## compare the performance of each prediction function
## test the selected parameters with part C


