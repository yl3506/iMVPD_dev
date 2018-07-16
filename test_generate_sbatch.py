## generate parallel scripts and submit to queue

# import necessary data
import MVPDroi_masterwrapper

# specify parameters
all_subjects = [1,2,3,4,5,6,9,10,14,15,16,17,18,19,20]
n_subject = len(all_subjects)
n_analysis = 
mvpd_dir = "/mindhive/saxelab3/anzellotti/software/" # TBD
parameters = {}
parameters['slurm'] = {}
parameters['slurm']['name'] = 'MVPDroi_iModels_facesVoices'
parameters['slurm']['time'] = 5 # in days
parameters['slurm']['cores_per_node'] = 5
parameters['slurm']['cpus_per_task'] = 1
parameters['slurm']['mem_per_cpu'] = 10240
parameters['slurm']['email'] = 'xxx@mit.edu'

# submit to queue 
