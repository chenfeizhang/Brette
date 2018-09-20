'''

Summarize the mean-std and mean-CV relation. Find the mean and std that reproduce expected firing rate and CV by hand.

'''

import numpy as np
import scipy.io as sio
import os.path

hostname = 'chenfei'
model = 'Brette'
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
outputdirectory = '%s/Output/'%(datafolder)
runs = 200

for tau in (50,): 
  for (spthr,posNa) in ((-35, 20),(-34, 40), (-30, 80)):
    for fr in (5,):
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = datafolder + 'Param/' + appendix  
      data = np.load(foldername + '/param.npy')
      param = data.item()
      thr = param['thr']
      mean =  []
      std = []
      cv = []
      for i in range(1,runs+1):
        if os.path.isfile(foldername+'/mean%d/std_mean_cv.npy'%(i)) == True:
          data = np.load(foldername+'/mean%d/std_mean_cv.npy'%(i))
          dic = data.item()
          mean.append(dic['mean'])
          std.append(dic['std'])
          cv.append(dic['cv'])
        else: continue

      if thr<0:
        spthr = 'n%d'%(abs(spthr))
      else:
        spthr = '%d'%(spthr)
      data_appendix = 'tau%sfr%sspthr%sposNa%s'%(tau, fr, spthr, posNa)
      sio.savemat(foldername+'_mean_std_cv',{'mean_%s'%(data_appendix):mean, 'std_%s'%(data_appendix):std, 'cv_%s'%(data_appendix):cv, 'thr_%s'%(data_appendix):thr})
