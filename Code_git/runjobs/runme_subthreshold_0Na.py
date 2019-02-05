'''

Generate axonal voltages and stimuli for calculating electrotonic filtering.

'''

import os, sys
from neuron import h
import numpy as np

# Load parameters
foldername = sys.argv[-1]
os.environ.keys()
i = int(os.environ['SGE_TASK_ID'])
print('i = %d'%(i))
data = np.load(foldername + '/param.npy')
param = data.item()
for key, val in param.items():
  exec(key + '=val')

# Import model simulation function and stimulus generation function.
sys.path.append('%s/Parameters'%(codedirectory))
from model_simulation_v import simulation, stimulate

T_all = T + T_relax # simulation time and randomization of initial condition time
L = int(T/dt) + 1
ftin = np.zeros(int(L/2+1))
ftout = np.zeros(int(L/2+1))
count = 0

for k in range(rep): 
  print('Loop at %d\n' %(k))
  seednumber = i*100+k # i is Series number. k is repitition number.
  [va, vs] = simulation(model, tau, posNa, T_all, 60, mean, std, dt=dt, seednumber=seednumber) # change the reset threshold to 60mV
  stim = stimulate([mean, std, tau, dt, T_all, seednumber])
  count = count + 1
  ftout = ftout + abs(np.fft.fft(va[int(T_relax/dt):])[:int(L/2+1)]/L)
  ftin = ftin + abs(np.fft.fft(stim[int(T_relax/dt):])[:int(L/2+1)]/L)

np.save(foldername + '/va_stim_%d'%(i), {'ftout':ftout, 'ftin':ftin, 'count':count})
