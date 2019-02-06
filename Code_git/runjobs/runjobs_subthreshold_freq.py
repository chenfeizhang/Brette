'''

This file calls runme_subthreshold_freq.py to generate axonal voltages and stimuli for calculating electrotonic filtering. Electrotonic filtering is defined as the Fourier transform of voltage trace not containing spikes to the Fourier transform of corresponding stimulus.

Neuron models are injected with sinusoidal stimuli ranged from 1Hz to 1000Hz.  

'''

import os, sys
import numpy as np
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette_soma10_0Na'  
runs = 1000 # number of jobs
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '/dyn_gain/scratch03/chenfei/%s/'%(model) # 
outputdirectory = '%s/Output/'%(datafolder)
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
  os.mkdir(outputdirectory)

sys.path.append('%s/scripts'%(codedirectory))
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
  os.mkdir(outputdirectory)

sys.path.append('%s/scripts'%(codedirectory))
from addparam import addparam # Import function addparam for loading parameters from IparamTable.txt.
IparamTableFile = '%s/Models/%s/IparamTable.txt'%(codedirectory,model) # txt file for stimulus parameters

# command for submitting jobs
queue_option = 'qsub -q fulla.q -q hel.q -q mvapich2-freya03.q -q mvapich2-freya02.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
script = 'runme_subthreshold_freq.py'
command = queue_option + ' ' + programme + ' ' + script

for tau in (5,): 
  for (thr,posNa) in ((20, 40),): 
    for fr in (5, ):
      param = {'tau':tau, 'fr':fr, 'posNa':posNa}
      param = addparam(param, IparamTableFile) # add thr, spthr, mean, std to param.
      param['T'] = 1000 # duration of model simulation for va (ms)
      param['T_relax'] = 1000 # duration of initial condition randomization (ms) # Note here it is 0!!
      param['rep'] = 1 # repetition number
      param['codedirectory'] = codedirectory   
      param['model'] = model 
      param['dt'] = 0.025
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, fr, param['thr'], posNa)
      foldername = datafolder + appendix + '_freq/' # appendix with subthreshold
      if os.path.isdir(foldername) == False:
        os.mkdir(foldername)
      np.save(foldername+'/param.npy', param)  
      call(command + ' ' + foldername, shell=True) 
   
        
