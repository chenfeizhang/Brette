'''

This file calls runme.py to run neuron model simulation and calculate spike triggered average (STA).

The mean and std of the stimulus are chosen to fix firing rate and coefficient variation (CV) of inter spike intervals. Stochastic stimulus always starts from its mean. Neuron voltage always starts with resting potential. Gating variable of sodium channels starts at corresponding voltage value.

In each job, the number of independent model simulation is denoted as rep. The duration of simulation time is T_relax+T. T_relax is the duration for randomization of initial condition. The duration of formal simulation is T.

The average of all spike triggered stimuli centered around corresponding spike times is the STA. The length of STA is denoted as STA_L. Spikes with a complete spike triggered stimulus interval within duration T are included for STA calculation.

Parameter definitions are the same with those in param_step1_runjobs.py

'''

import os, sys
import numpy as np
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette'  
runs = 10 # number of jobs
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
outputdirectory = '%s/Output/'%(datafolder)
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
  os.mkdir(outputdirectory)

sys.path.append('%s/scripts'%(codedirectory))
from addparam import addparam # Import function addparam for loading parameters from IparamTable.txt.
IparamTableFile = '%s/Models/%s/IparamTable.txt'%(codedirectory,model) # txt file for stimulus parameters

# command for submitting jobs
queue_option = 'qsub -q fulla.q -q openmp-fulla01.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/runjobs/runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script   

for tau in (5, ): 
  for posNa in (20,): 
    for fr in (5,):
      param = {'tau':tau, 'fr':fr, 'posNa':posNa}
      param = addparam(param, IparamTableFile) # add thr, spthr, mean, std to param.
      param['T'] = 20000 # duration of model simulation for STA (ms)
      param['T_relax'] = 500 # duration of initial condition randomization (ms)
      param['rep'] = 10 # repetition number
      param['codedirectory'] = codedirectory   
      param['model'] = model 
      param['dt'] = 0.025
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, fr, param['thr'], posNa)
      foldername = datafolder + appendix
      if os.path.isdir(foldername) == False:
        os.mkdir(foldername)
      # make directory for bootstrapping confidence interval
      if os.path.isdir(foldername+'/bootstrapping') == False:
        os.mkdir(foldername+'/bootstrapping')
      # make directory for null hypothesis test
      if os.path.isdir(foldername+'/nullhypothesis') == False:
        os.mkdir(foldername+'/nullhypothesis')
      for i in range(1,runs+1):
        call('mkdir -p ' + foldername + '/Series' + str(i) + '/', shell=True) 
      np.save(foldername+'/param.npy', param)        
      call(command + ' ' + foldername, shell=True) 
   
        
