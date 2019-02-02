'''

Collect data and calculate electrotonic filtering. 

'''

hostname = 'chenfei'
model = 'Brette'  
runs = 500
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '/dyn_gain/scratch03/chenfei/%s/'%(model)
import numpy as np
import scipy.io as sio

for tau in (5,): # 20
  for (thr,posNa) in ((-19, 0),(-23, 20),(-18, 40),(-8, 80),): 
    for fr in (5, ):
      appendix = 'tau%dfr%dthreshold%dposNa%s'%(tau, fr, thr, str(posNa))
      foldername = datafolder + appendix + '_subthreshold/' # appendix with subthreshold
      data = np.load(foldername + 'param.npy')
      dic = data.item()
      T = dic['T'] # duration of simulation (ms)
      dt = dic['dt'] # time step (ms)
      L = int(T/dt) + 1
      ftin = np.zeros(int(L/2+1))
      ftout = np.zeros(int(L/2+1))
      n_all = 0
      for i in range(1, runs+1):
        data = np.load(foldername + 'va_stim_%d.npy'%(i))
        dic = data.item()
        n_all = n_all + dic['count']
        ftin = ftin + dic['ftin']
        ftout = ftout + dic['ftout']

      gain = abs(ftout/ftin)
      print('n_all is %s'%(n_all))
      sf = 1/(dt/1000.0)
      f = sf/2*np.linspace(0,1,L/2+1)
      sio.savemat(foldername + 'electrotonic_filtering', {'g_tau5_posNa%d'%(posNa):gain[1:], 'f':f[1:]})
      
