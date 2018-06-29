import os, json
import nibabel as nib
import numpy as np
from sklearn import linear_model

# load mask and img data
mask = nib.load('aal.nii.gz')
mask_data = mask.get_data()
img_a = nib.load('sub-18_ses-movie_task-movie_run-1_bold_space-T1w_preproc.nii.gz')
img_b = nib.load('sub-17_ses-movie_task-movie_run-1_bold_space-T1w_preproc.nii.gz')
img_a_data = img_a.get_data()
img_b_data = img_b.get_data()
print("mask_data shape")
print(mask_data.shape)
img_a_data_shape = img_a_data.shape
print("img_a_data shape")
print(img_a_data.shape)
img_b_data_shape = img_b_data.shape
print("img_b_data shape")
print(img_b_data.shape) # a and b might be of different shape

# resize mask: select sub-matrix to match shape of img
mask_data_a=mask_data[80:129,100:161,80:128]
mask_data_b=mask_data[80:128,98:155,81:126]
print("mask_data shape after resize")
print(mask_data_a.shape)
print(mask_data_b.shape)
# check number of voxels with certain label
mask_a_label = 8
print("number of label 8") 
num_label_a = np.count_nonzero(mask_data_a==mask_a_label)
print(num_label_a)
mask_b_label = 2
print("number of label 2") 
num_label_b = np.count_nonzero(mask_data_b==mask_b_label)
print(num_label_b)

# generate mask
mask_a = mask_data_a == mask_a_label
mask_b = mask_data_b == mask_b_label

# apply mask on img_data
a = np.zeros((img_a_data_shape[3],num_label_a+1)) # initialize region a
b = np.zeros((img_b_data_shape[3],num_label_b)) # initialize region b

# iterate through img_a_data with mask_a
a_index = 0
for t in range(0, img_a_data_shape[3]):
	a[t, a_index] = 1 # bias term
	a_index += 1
	for x in range(0, img_a_data_shape[0]):
		for y in range(0, img_a_data_shape[1]):
			for z in range(0, img_a_data_shape[2]):
				if mask_a[x,y,z]: # if mask true
					print("xyzt, a_index: %d" % a_index)
					print('x = %d' % x)
					print('y = %d' % y)
					print('z = %d' % z)
					print('t = %d' % t)
					print('a = %f' % img_a_data[x, y, z, t])
					a[t, a_index] = img_a_data[x, y, z, t]
					a_index += 1				
	a_index = 0 # reset column index

# iterate through img_b_data with mask_b
b_index = 0
for t in range(0, img_b_data_shape[3]):
	for x in range(0, img_b_data_shape[0]):
		for y in range(0, img_b_data_shape[1]):
			for z in range(0, img_b_data_shape[2]):
				if mask_b[x,y,z]:
					print("xyzt, b_index: %d" % b_index)
					print('x = %d' % x)
					print('y = %d' % y)
					print('z = %d' % z)
					print('t = %d' % t)
					print('b = %f' % img_b_data[x, y, z, t])
					b[t, b_index] = img_b_data[x, y, z, t]
					b_index += 1				
	b_index = 0 # reset column index

# check if region data is correctly masked
print(a)
print(b)

# linear regression step
# split datasets into training and testing sets
a_train = a[:img_a_data_shape[3] - 50, :]
a_test = a[img_a_data_shape[3] - 50:, :] 
b_train = b[:img_b_data_shape[3] - 50, :]
b_test = b[img_b_data_shape[3] - 50:, :]
# check if the split is in correct size
print(a_train.shape)
print(a_test.shape)
# initialize linear regression model
print("try linear regression model")
regr = linear_model.LinearRegression() # with default settings
# fit in training sets
regr.fit(a_train, b_train)
# get coefficients of the training resutl
print(regr.coef_)
# testing
predict_lin = regr.predict(a_test)
# check with the answer and calculate error (squared)
err_lin = predict_lin - b_test
print('squared error: %f' % np.sum(err_lin * err_lin))
print('b_test * b_test: %f' % np.sum(b_test * b_test))

# now try regularization model
clf = linear_model.MultiTaskElasticNetCV()
clf.fit(a_train, b_train)
predict_clf = clf.predict(a_test)
err_clf = b_test - predict_clf
print("squared error: %f" % np.sum(err_clf * err_clf))
print("b_test * b_test: %f" np.sum(b_test * b_test))