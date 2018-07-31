### main execution function
import os
import load_data, generate_script, interaction_model

## environment and input setup
# import necessary libraries and variables
# specify the input, and parameters
data_main_directory = '/Users/chloe/Documents/data_test/'
data_preprocessed_dir = data_main_directory + 'processed/'
data_model_out_dir = data_main_directory + 'model_out/'
all_sub_list = [] # list of all subjects

# iterate through the folder and save all subjects into list
os.chdir(data_main_directory)
all_data_files = os.listdir('.') # list all files in current
all_sub_list = [] # list of all subjects' directories after preprocessing
for data_file in all_data_files: 
	# filter to select subject folders only
	if 'sub-' in data_file:
		# if encounter a subject folder, preprocess it, and save result to new folder
		preprocess(data_main_directory+data_file, data_preprocessed_dir)
		all_sub_list.append(data_file)

# iterate through all subject and list all possible combinations
all_combinations = [] 
for sub1_index in range(0, len(all_sub_list) - 1):
	for sub2_index in range(sub1_index + 1, len(all_sub_list)):
		all_combinations.append([all_sub_list[sub1_index], all_sub_list[sub2_index]])
		all_combinations.append([all_sub_list[sub2_index], all_sub_list[sub1_index]])

# iterate through all combinations and launch interaction model 
for combination in all_combinations:
	interaction_model_linear(combination[0], combination[1], data_preprocessed_dir, data_model_out_dir, 5, 0.005)
	# the output is automatically saved to data_model_out_dir

