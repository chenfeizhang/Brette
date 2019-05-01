'''

Determine bootstrapping boundaries from 1000 bootstrapping linear response curves.

Linear response curves should be calculated with transferit.py before running this file.

'''

import numpy as np
import scipy.io as sio

hostname = 'chenfei'
model = 'Brette_soma1250_L2'
runs = 1000
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '/dyn_gain/scratch01/chenfei/%s/'%(model)

for tau in (5, ): 
  for (thr,posNa) in ((-18,40),):
    for fr in (5, ): 
      appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
      foldername = datafolder + appendix
      gain = []
      # Load linear response curves
      for i in range(1,runs+1):
        data = np.load(datafolder+appendix+'/bootstrapping/transferdata_bootstrapping_%d.npy'%(i))
        dic = data.item()
        gain.append(dic['gain'])
      
      # Sort all curves to determine the 95 percent boundary.
      gain_all = np.array(gain)
      gain = np.sort(gain_all, axis=0)
      bootstrapping_gain_lower = gain[int(runs*0.025)] # take the 95 percent in the middle as the confidence interval
      bootstrapping_gain_upper = gain[int(runs*0.975)]
      if thr<0:
        thr = 'n%d'%(abs(thr))
      else:
        thr = '%d'%(thr)
      data_appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
      data = sio.loadmat(datafolder+'dynamic_gain_Hz_per_nA_%s.mat'%(data_appendix))
      data['bootstrapping_gain_lower_%s'%(data_appendix)] = bootstrapping_gain_lower
      data['bootstrapping_gain_upper_%s'%(data_appendix)] = bootstrapping_gain_upper
      # Save bootstrapping boundaries in linear response curve data file.
      sio.savemat(datafolder+'dynamic_gain_Hz_per_nA_%s'%(data_appendix), data)
