'''

This file is called after VClamp_runjobs.py. Save data into one file.

'''

import numpy as np
import scipy.io as sio

hostname = 'chenfei'
model = 'Brette'
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
runs = 1000

for posNa in (20, ): 
  appendix = 'posNa%s'%(posNa)
  foldername = datafolder + 'VClamp/' + appendix  
  va_all = []
  vs_all = []
  m_all = []
  for i in range(1, runs+1):
    data = np.load(foldername+'/VClamp_run_%d.npy'%(i))
    data = data.item()
    va_all.append(data['va'])
    vs_all.append(data['vs'])
    m_all.append(data['m'])
  sio.savemat(datafolder + 'VClamp/' + appendix + '_va_vs_m', {'va':va_all, 'vs':vs_all, 'm':m_all})
