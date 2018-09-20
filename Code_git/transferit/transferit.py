'''

Calculation of the linear response function with the STA

Self-test script calculates the linear response function of Brette model with posNa=20um, tau=5ms, fr=5Hz. The final STA is averaged over all 400 jobs.

'''


def STA_average(List, datafolder, appendix):
  '''

  This function averages STAs over different jobs to get the final STA for linear response function.
  List: a list of job indices for STA average.
  datafolder: directory of data
  appendix: appendix for neuron model and stimulus parameters

  '''
  import numpy as np
  import os
  file_number=0 # total file number
  data = np.load(datafolder + appendix + '/param.npy')
  param = data.item()
  L = param['L']
  STA = np.zeros(L)  
  for k in List:
    datafile = datafolder + appendix + '/Series%s/STA.npy'%(k)
    if os.path.isfile(datafile) == True:
      STA_nspikes = np.load(datafile)
      STA_nspikes_dict = STA_nspikes.item()       
      STA_tmp = STA_nspikes_dict['STA']
      STA = STA + STA_tmp  
      file_number += 1
    else: continue 
  print("Total file number is %s"%(file_number))     
  STA = STA/float(file_number) # averaged STA over 400 jobs
  return STA


def gain(STA, datafolder, appendix):
  '''
  
  This function calculates the linear response curve based on final STA and parameters of stimulus.

  The linear response curve is a ratio of Fourier transform of STA to power spectral density of stimulus.

  '''
  import numpy as np
  import math
  data = np.load(datafolder + appendix + '/param.npy')
  param = data.item()
  for key, val in param.items():
    exec(key + '=val')

  f = sf/2*np.linspace(0,1,L/2+1) # frequency
  idx = 2000 # length of the dynamic gain components to be shown
  # filter STA with a trapezoid shaped fileter, such that two ends of STA are zero. This suppresses the noise in Fourier transform. 
  sidelength = 0.05 
  side = np.arange(0,1+dt_s/sidelength, dt_s/sidelength) # A linear slope of width 0.05 and hight 1
  window = np.array(list(side) + list([1]*(L-2*len(side))) + list(1-side))
  STA = STA*window # make the STA begin and end with 0
  ftSTA = np.fft.fft(np.append(STA[L/2:], STA[0:L/2]))/float(L) 
  ftSTA = ftSTA[0:L/2+1] 
  psd = 2*tau*(10**-3)*(std**2)/(1+(2*math.pi*tau*10**-3*f)**2) # analytical form of the power spectral density of the OU process stimulus
  gain_filt = np.zeros(idx)
  for i in range(idx):
    if i == 0:
      g = np.array([0]*len(ftSTA))
      g[0] = 1 # The fileter doesn't change the first component of ftSTA.
    else:
      g = math.e**(-2*math.pi**2*(f-f[i])**2/f[i]**2) # Gaussian filters, the variance increase with the frequency.
      g = g/float(sum(g)) # Normalize the filter to have a sum of one.
    gain_filt[i] = abs(sum(ftSTA*g))/float(psd[i]) # filter out the noise in the high frequency components

  return f[range(idx)], gain_filt


# self-test
if __name__ == '__main__':
  import numpy as np
  import scipy.io as sio

  hostname = 'chenfei'
  model = 'Brette'
  runs = 400
  datafolder = '../dyn_gain/%s/'%(model)

  for tau in (5, ): 
    for (thr,posNa) in ((-23,20),): 
      for fr in (5, ):
        appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
        STA = STA_average(range(1, runs+1), datafolder, appendix) # averaged STA
        [f, gain_filt] = gain(STA, datafolder, appendix) 
        if thr<0:
          thr = 'n%d'%(abs(thr))
        else:
          thr = '%d'%(thr)               
        transferdata = {'f':f, 'gain_tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa):gain_filt}
        sio.savemat(datafolder+'transferdata_tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa), transferdata)

