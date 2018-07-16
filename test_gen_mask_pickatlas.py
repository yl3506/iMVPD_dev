import os
import numpy as np
import matplotlib.pyplot as pyplot
from sklearn.linear_model import ElasticNetCV

# load raw func data 
a = np.random.random((2,3,4,5)) # 90x90x90x196
# generate a_mask of boolean
a_mask = np.zeros((2,3,4,5)) # 90x90x90x196
b_mask = np.zeros((2,3,4,5))
a_mask[0,0,0,0]=1
a_mask[0,0,0,1]=1
a_mask[0,0,0,2]=1
a_mask[0,0,0,3]=1
a_mask[0,0,0,4]=1
a_mask[0,0,1,0]=1
a_mask[0,0,1,1]=1
a_mask[0,0,1,2]=1
a_mask[0,0,1,3]=1
a_mask[0,0,1,4]=1
b_mask[1,2,3,0]=1
b_mask[1,2,3,1]=1
b_mask[1,2,3,2]=1
b_mask[1,2,3,3]=1
b_mask[1,2,3,4]=1
b_mask[1,2,2,0]=1
b_mask[1,2,2,1]=1
b_mask[1,2,2,2]=1
b_mask[1,2,2,3]=1
b_mask[1,2,2,4]=1
a_mask=a_mask==1
b_mask=b_mask==1
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
# print data for debug
print("a_train")
print(a_train)
print("b_train")
print(b_train)
print("a_validate")
print(a_validate)
print("b_validate")
print(b_validate)
print("a_test")
print(a_test)
print("b_test")
print(b_test)



