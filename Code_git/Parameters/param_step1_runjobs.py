''' 

Search for constant input to realize expected firing rate.

Current file defines model name and parameters, calls param_step1_runme.py, and submits jobs to clusters for constant input searching. 

With the knowledge of spike time threshold, temporarily choose reset threshold slightly larger than spike time threshold. Search for the constant input based on the temporary reset threshold. Final reset threshold is defined as the axonal voltage 2ms after the spike time threshold under the constant input.

'''
import numpy as np
import os
from subprocess import call 

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette' # model name
codedirectory = '/home/%s/Code_git'%(hostname) # code directory
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model) # data directory
outputdirectory = '%s/Output/'%(datafolder) # output directory

# command for submitting jobs
queue_option = 'qsub -q hel.q -b y -j y -cwd -o %s' %(outputdirectory)
programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/Parameters/param_step1_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script    

# Make directories for data and output files.
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
if os.path.isdir(outputdirectory) == False:
  os.mkdir(outputdirectory)
rootfolder = datafolder + 'Param/'
if os.path.isdir(rootfolder) == False:
  os.mkdir(rootfolder)

# Define parameters and submit jobs to clusters.
# tau: correlation time of stimulus (ms)
# thr: reset threshold (mV)
# spthr: spike time threshold (mV)
# posNa: position of sodium channels (um)
# fr: firing rate (Hz)
# leftI: lower bound of constant stimulus searching range (nA)
# rightI: upper bound of constant stimulus searching range (nA)
# precisionFiringOnset: precision of stimulus searching
# T: duration of stimulus and simulation (ms)
# dt: time step of model simulation (ms)

for tau in (5, 50):
  for (thr, spthr, posNa) in ((-34, -35, 20),(-33, -34, 40),(-29, -30, 80)): 
    for fr in (5,): 
      leftI = 0.00001 # chosen by hand
      rightI = 0.05 # chosen by hand
      precisionFiringOnset = 1e-2 # Searching stops when the upper and lower bounds are close enough.
      T = 20000 
      dt = 0.025
      param = {}
      param['tau'] = tau
      param['thr'] = thr
      param['spthr'] = spthr
      param['posNa'] = posNa
      param['fr'] = fr
      param['T'] = T
      param['codedirectory'] = codedirectory   
      param['model'] = model 
      param['leftI'] = leftI
      param['rightI'] = rightI
      param['precisionFiringOnset'] = precisionFiringOnset
      param['dt'] = dt
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = rootfolder + appendix
      param['foldername'] = foldername
      call('mkdir -p ' + foldername, shell=True) 
      np.save(foldername+'/param', param) # save data in param.npy
      call(command + ' ' + foldername, shell=True) # Submit jobs, pass foldername into the job script.



