'''

Collect data and calculate electrotonic filtering. 

'''

hostname = 'chenfei'
model = 'Brette_soma10_0Na'  
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '/dyn_gain/scratch03/chenfei/%s/'%(model)
import numpy as np
import scipy.io as sio

for tau in (5,): # 20
  for (thr,posNa) in ((20, 40),): 
    for fr in (5, ):
      f = []
      gain = []
      for frequency in range(1, 1001):
        appendix = 'tau%dfr%dthreshold%dposNa%s'%(tau, fr, thr, str(posNa))
        foldername = datafolder + appendix + '_freq/'
        data = np.load(foldername + 'freq_%d.npy'%(frequency))
        dic = data.item()
        f.append(frequency)
        gain.append(dic['ftout'])
      dataname = datafolder + 'freq_tau%d_fr%d_posNa%d'%(tau, fr, posNa)
      sio.savemat(dataname, {'f':f,'g_posNa%d'%(posNa):gain})
      
