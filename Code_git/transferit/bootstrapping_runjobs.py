'''

Calculate confidence intervals of linear response curves.

This file calls bootstrapping_runme.py and creates 1000 jobs for bootstrapping. For each bootstrapping, it randomly select STA files from series folder with replacement. The total number of STAs is the same with than in runjobs.py. Linear response curves are calculated with the randomly selected STAs.

Bootstrapping boundary is the middle 95 percent range of 1000 curves. The boundary is determined by bootstrapping_step2.py.

'''

from subprocess import call

hostname = 'chenfei'
model = 'Brette'
runs = 1000
codedirectory = '/home/%s/Code_git'%(hostname)
datafolder = '%s/dyn_gain/%s/'%(codedirectory, model)
outputdirectory = '%s/Output/'%(datafolder)

queue_option = 'qsub -q hel.q -q fulla.q -q openmp-fulla01.q -t 1:%d:1 -b y -j y -o %s' %(runs, outputdirectory)
programme = 'python'
script = '%s/transferit/bootstrapping_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script    
call(command + ' ' + datafolder, shell=True)


