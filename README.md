# MVPD_Intersubject
Multivariate Pattern Dependence on inter-subject model.<br />
The project is based on previous work of MVPD ([Anzellotti S, Caramazza A, Saxe R (2017) Multivariate pattern dependence. PLoS Comput Biol 13(11): e1005799. https://doi.org/10.1371/journal.pcbi.1005799](http://journals.plos.org/ploscompbiol/article?rev=2&id=10.1371/journal.pcbi.1005799))

## Code Workflow
### Reorganize dataset to match BIDS specification
The original dataset we are using is [StudyForrest](http://studyforrest.org/data.html)<br />
We need to reorganize it to match [BIDS format](http://bids.neuroimaging.io/bids_spec1.1.0.pdf)
- BIDS_arrange_file.py

>	Add description file (dataset_description.json) in the dataset main directory.<br />
	Move corresponding data files to two session directories: ses-localizer, ses-movie.<br />
	Move corresponding files to ses-localizer/func/, ses-localizer/anat/, ses-movie/func/, and ses-movie/anat/ directories.<br />
	Rename 'T1w_defacemask' files.<br />
	Delete empty directories.<br />
- BIDS_add_ses_tag.py
	
>	Add session label to the files in anat/ directories.
- BIDS_rename_anat_files.py
	
>	Modify 'defacemask' files name.
- BIDS_add_repetition_time.py
	
>	Add 'RepetitionTime' and 'TaskName' information to the json files.

### Preprocess dataset using FMRIPREP
Normalize the reorganized dataset by FMRIPREP.<br /> 
Detailed tutorial can be found on [From Percepts To People Laboratory](http://fptp.wikidot.com/wiki:fmri-preprocessing-tutorial)

### Generate ROIs using FEAT and FSL
- roi_object_events.py

>	Create time sheet for each localizer session, needed for FEAT analysis.
- Analyze data using FEAT & FSL

>	Create general ROIs of 'face', 'scene', 'body', 'house', 'object', or 'scramble' regions.<br />
	[FEAT & FSL Documentation](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL)
- roi_gen_face_ROIs.py

>	Generate specific face ROIs from the general ROI masks by creating a sphere around the peak and pick the maximum 80 voxels.<br />
	Prerequisite: You have the general masks of face regions already in the correct size. In our case, the general masks are in the 'kanparcel' directory.

### Filter out necessary data
- data_filter_roi.py

>	Filter out ROI data and save as numpy file (t x v matrix).<br />
- data_filter_noise.py

>	Filter out WhiteMatter and CSF data and save as numpy file. Preperation for compcorr denoising.<br />
	Prerequisite: You have the masks for WhiteMatter and CSF already in the correct size.
- data_filter_cos.py

>	Filter out confound cosine data and save as numpy file. Preperation for denoising.
- data_filter_xyz.py

>	Filter out confound xyz translation and rotation data and save as numpy file. <br />
	Preperation for denoising.

### Denoising
- denoise_model_cos.py
	
>	Denoise using only confound cosine data as predictor, and save denoised/real data to decosed/ directory.
- denoise_model_compcorr.py

>	Denoise using confound cosine (first step) and compcorr (second step), and save denoised/real data to decosed_compcorr/ directory.
- denoise_model_xyz.py

>	Denoise using confound cosine (first step) and xyz translation and rotation data (second step), and save denoised/real data to decosed_dexyz/ directory.

### Normalizing and demeaning
- denoise_normalize.py

>	Normalize data as ratio of variance fluctuated. <br />
	Remember to repeat this step for 3 denoising models: cos, cos+xyz, cos+compcorr.
- denoise_demean_normalized.py	

>	Remove mean of each voxel of data after normalizing. <br />
	Remember to repeat this step for 3 denoising models: cos, cos+xyz, cos+compcorr.

### PCA modeling
Prediction model for each subject pair and each ROI pair (including within and inter subject, within and cross region).
Method used is [PCA from SKLearn](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
- model_pca_all.py
	
>	Data used is after cos+compcorr.<br />
	Remember to repeat for 1, 2, and 3 components, by which we can pick the optimal number of components to use for future analysis.

### Figure 1: visualize component performance
- accuracy_correlation.py
	
>	Generate correlation for each prediction, which is the sqrt(var explained raw).<br />
	Remember to repeat for 1, 2, and 3 components.
- accuracy_correlation_chart.py
	
>	Generate correlation chart for each subject (of all region pairs).<br />
	Remember to repeat for 1, 2, and 3 components.
- visualize_within_corr_overall.py
	
>	Visualize the performance for 1, 2, and 3 component models by showing average correlation explained. <br />
	Remember to repeat for 1, 2, and 3 components.

Now we can compare the figures and find the optimal number of components(#pc), idealy 3.
Next we would like to find the good subjects which have less noise.
- accuracy_raw_ratio_chart_within.py

>	Generate raw variance explained chart for each within subject prediction (with #pc).
- visualize_within_raw.py

>	Visualize within subject performance (var explained raw) for each subject.<br />
	Then we can compare the subject performances and pick the good ones.

### Figure 2: compare within and inter performance
We only use the good subjects and number of components onwards.
- accuracy_same_region_var.py

>	Take the average of raw variance explained of the same region prediction (both within subject and inter subject).
- accuracy_ceil_ratio.py

>	Generate the variance explained as ratio to the ceiling for each prediction.
- accuracy_ceil_ratio_chart_within.py

>	Generate the ceiling ratio chart for each within subject prediction.
- accuracy_ceil_ratio_chart_cross.py

>	Generate the ceiling ratio chart for each inter subject prediction.
- visualize_same_region.py

>	Create the comparison histogram of same region prediction performance between inter subject and within subject.
- visualize_within_ceil_overall.py

>	Create the matrix of within subject performance (as ratio to the ceiling). <br />
	The diagonal is set to NaN.
- visualize_cross_ceil_overall.py

>	Create the matrix of inter subject performance (as ratio to the ceiling). <br />
	The diagonal is set to NaN.

### Figure 3: compare denoising performance
- model_pca_all.py
	
>	Prediction model for each subject pair and ROI pair.<br />
	Remember to repeat for cos, cos+xyz.
- accuracy_raw_ratio_chart_cross.py

>	Generate raw variance explained chart for each subject pair.<br />
	Remember to repeat for cos, cos+xyz, cos+compcorr.
- visualize_vs_raw_overall.py

>	Create matrix of difference of raw variance explained performance of within and inter subject.<br />
	Remember to repeat for cos, cos+xyz, and cos+compcorr.

### Figure 4: PCA of performance results
To find the relation between networks by PCA raw variance explained performance.
- accuracy_sub_vector.py
	
>	Generate vector of all region pair prediction performance (variance explained raw) for each subject.
- visualize_vector_mean.py

>	Create a matrix of the mean of each vector generated above.
- visualize_vector_pca.py

>	Implement PCA on all vectors (pc=2).<br />
	Create a coordinate figure of all subject pair projections on the components.<br />
	Create a matrix of the first component weight of each feature (region pair).<br />
	Create a matrix of the second component weight of each feature (region pair).



	




