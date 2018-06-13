import os
import numpy as np

# load raw func data 
a = np.random.random((2,3,4,5)) # 90x90x90x196
# generate a_mask of boolean
a_mask = np.zeros((2,3,4,5)) # 90x90x90x196
b_mask = np.zeros((2,3,4,5))
# apply the mask to our dataset, may need iteration through all time points
a_data = a[a_mask] # 96x1000
b_data = a[b_mask]
# reshape
a_data = np.reshape(a_data, (2,5)) # 1000x196
b_data = np.reshape(b_data, (2,5))
# transpose
a_data = np.transpose(a_data) # 196x1000
b_data = np.transpose(b_data)
# split data to train/validate/test sets
a_split = np.split(a_data, [3,4,5]) # ending indices
b_split = np.split(b_data, [3,4,5])
a_train = a_split[0]
a_validate = a_split[1]
a_test = a_split[2]
b_train = b_split[0]
b_validate = b_split[1]
b_test = b_split[2]