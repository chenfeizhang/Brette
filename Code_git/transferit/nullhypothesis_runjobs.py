'''

Calculate null hypothesis test curve.

This file calls nullhypothesis_runme.py. For each series folder, reproduce the stimuli that generate spikes for each simulation duration T in runme.py. Load corresponding spike times in T, add a random number to all spike times and mod them by T. In this way, the spike times are shuffled, but the spiking pattern (CV of ISI) is kept. Calculate STA and linear response curve with shuffled spike times. Repeat this procedure 500 times to get 500 linear response curves. Final null hypothesis test curve is the 95 percent upper bound of these curves. Reducing the repetition time to 100 provides a similar result, except that the curve is more noisy.

In figures of our paper, only the linear response curves above the null hypothesis test curves are shown. Null hypothesis test curves are not shown.

'''

from subprocess import call

hostname = 'chenfei'
model = 'Brette_soma1250_L2'
runs = 400 # number of series folders
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '/dyn_gain/scratch01/chenfei/%s/'%(model)
outputdirectory = '%s/Output/'%(datafolder)

queue_option = 'qsub -q fulla.q -q openmp-fulla01.q -q hel.q -t 1:%d:1 -b y -j y -o %s' %(runs, outputdirectory)
programme = 'python'
script = '%s/transferit/nullhypothesis_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script  
 
for tau in (5,): #  
    for (thr,posNa) in ((-18, 40),): # 
      f = 5 
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, f, thr, posNa)
      foldername = datafolder + appendix
      call(command + ' ' + foldername , shell=True)    
