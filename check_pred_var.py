import numpy as np
import os

main_dir = '/mindhive/saxelab3/anzellotti/forrest/output_denoise_normalized/sub-02_to_sub-03/'
os.chdir(main_dir)
for file in os.listdir('.'):
	os.chdir(file)
	for run in range(1, 9):
		pred = np.load(main_dir + 'run_' + str(run) + '_regularization_predict_001.npy')
		# iterate through all voxels
		for v in range(0, pred.shape[1]):
			var = pred[:, v].var()
			if var < 0.00002:	
				if var == 0:
					print('warning')
				print('run ' + str(run) + ' voxel ' + str(v) + ' is : ' + str(var))
