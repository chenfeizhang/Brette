'''

Collect data and calculate impedance. 

'''

hostname = 'chenfei'
model = 'Brette'  
runs = 100
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
import numpy as np
import scipy.io as sio

for tau in (5,): # 20
  for (thr,posNa) in ((-23, 20),): 
    for fr in (5, ):
      appendix = 'tau%dfr%dthreshold%dposNa%s'%(tau, fr, thr, str(posNa))
      foldername = datafolder + appendix + '_subthreshold/' # appendix with subthreshold
      T = 400 # duration of simulation (ms)
      dt = 0.025 # time step (ms)
      L = int(T/dt) + 1
      ftin = np.zeros(int(L/2+1))
      ftout = np.zeros(int(L/2+1))
      n_all = 0
      for i in range(1, runs+1):
        data = np.load(foldername + 'va_stim_%d.npy'%(i))
        n = data.shape[0]
        print('n is %s'%(n))
        n_all = n_all + n
        for j in range(n):    
          ftin = ftin + (np.fft.fft(data[j, L:])[:int(L/2+1)]/L)
          ftout = ftout + (np.fft.fft(data[j, :L])[:int(L/2+1)]/L)
      freq = np.fft.fftfreq(L, dt/1000.0)[:int(L/2+1)]
      gain = abs(ftout/ftin)/n_all
      sio.savemat(foldername + 'data', {'gain':gain, 'f':freq})
      
