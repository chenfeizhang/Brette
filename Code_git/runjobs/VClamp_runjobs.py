'''

This file calls VClamp_runme.py to calculate the stationary axonal voltage and gating variable of sodium channels under voltage clamp at soma.

'''

import os
import numpy as np
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette'
runs = 1000 # number of jobs
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
outputdirectory = '%s/Output/'%(datafolder)
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
if os.path.isdir(outputdirectory) == False:
  os.mkdir(outputdirectory)
rootfolder = datafolder + 'VClamp/'
if os.path.isdir(rootfolder) == False:
  os.mkdir(rootfolder)

# command for submitting jobs
queue_option = 'qsub -q fulla.q -q hel.q -q openmp-fulla01.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
script = 'VClamp_runme.py'
command = queue_option + ' ' + programme + ' ' + script    

for posNa in (20,): 
  appendix = 'posNa%s'%(posNa)
  foldername = datafolder + 'VClamp/' + appendix  
  param = {}
  param['posNa'] = posNa
  param['codedirectory'] = codedirectory   
  param['model'] = model 
  if os.path.isdir(foldername) == False:
    os.mkdir(foldername)
  np.save(foldername+'/param', param)
  call(command + ' ' + foldername, shell=True)  

