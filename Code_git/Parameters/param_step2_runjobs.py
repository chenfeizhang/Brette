'''

For a given mean of the stimulus, search for the std of the stimulus that generates expected firing rate. Finishing param_step1_runjobs.py is required before running this file.

Current file defines model name and parameters, calls param_step2_runme.py, and submits jobs to clusters for std searching. 

Parameter definitions are the same with those in param_step1_runjobs.py

'''

import numpy as np
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette'
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
outputdirectory = '%s/Output/'%(datafolder)

# command for submitting jobs
runs = 100 # number of jobs, number of different mean values for std searching
queue_option = 'qsub -q hel.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/Parameters/param_step2_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script  

for tau in (5,): 
  for (spthr,posNa) in ((-35, 20),): 
    for fr in (5,): 
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = datafolder + 'Param/' + appendix
      data = np.load(foldername + '/param.npy')
      param = data.item() 
      param['leftStd'] = 0.00000001 # lowerbound
      param['rightStd'] = 0.5 # upperbound
      param['precision_std'] = 1e-3 # relative error for parameter searching
      np.save(foldername+'/param', param)
      for i in range(1,runs+1):
        call('mkdir -p ' + foldername + '/mean'+str(i), shell=True)
      call(command + ' ' + str(runs) + ' ' + foldername, shell=True) # Submit jobs, pass runs and foldername into the job script.
