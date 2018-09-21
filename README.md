# Python Code for Neuron Model Simulation and Linear Response Function Calculation:

The Python code here simulates a simple multi-compartment model proposed by [Brette 2013](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003338) and calculates its linear response functions which describe the population encoding ability of the neuron model. 

It first provides a procedure to determine the axonal voltages for spike time detection and voltage reset to finish a spike. It also provides a parameter searching procedure to determine mean and std of stochastic stimulus which reproduce expected firing rate and coefficient variation (CV) of iter-spike intervals (ISI) of the neuron model. Thirdly, it implements the methods proposed by [Higgs et al. 2009](http://www.jneurosci.org/content/29/5/1285.long) to calculate the linear response functions of the neuron model which shows the impact of neuron morphology, spike initiation dynamics and stimulus properties on population encoding abilities. In the last part, it provides a procedure for calculating bootstrapping confidence intervals and null hypothesis test curves. This is the code for our [manuscript](https://arxiv.org/abs/1807.00509). 

## 1. How to Get Started

To run the code, we used Python 2.6 complied with NEURON 7.3. Some scripts are run on the cluster. Place the code folder Code_git in home directory, go to directory ```~/Code_git/Models/Brette```. Compile the mod file with command ```nrnivmodl```. The other two directories ```Brette_ka01``` and ```Brette_soma10_ka01``` contain neuron models with different parameter setup. For ```Brette_ka01```, parameter $[k_{a}]$ and ```Brette_soma10_ka01```

Compile corresponding mod files before running simulations with these models. 

## 2. Determine Axonal Voltage for Spike Time Dectection

Brette model is a simple multi-compartment model composed of a soma and an axon. Only sodium channels are located at point on the axon for spike generation (AP initiation site). The rest of the neuron model is passive. To finish a spike, it requires to reset the voltage by hand when the axonal voltage at the AP initiation site reaches some specific value. We call this reset threshold. To determine the spike time, we choose the axonal voltage with the maximum voltage derivative for spike time dectection.

model_simulation.py in ```~/Code_git/Parameters``` provides a function for model simulation and a function for stimulus generation. It also provides self-test code to run model simulation with the following command:

```
~/Code_git/Models/Brette/x86_64/special -python model_simulation.py Brette
```
To determine spike time dectection voltage at the AP initiation site, we first set reset threshold to the reserval potential of sodium channels, which is 60mV. Injecting the soma with a constant stimulus of appropriate size, choose the axonal voltage with the maximum voltage derivative as the spike detection voltage. The stimulus size should be large enough to make axonal voltage pass half-activation voltage of sodium channels, which is -40mV. It also shouldn't be too large to make the voltage larger than the reserval potential. Spike detection voltage is quite insensitive to the constant stimulus amplitude. In fact, the axonal voltages around the spike detection voltage will usually fall in the same time bin during the simulation, which will not affect spike time detection.


## 3. Determine mean and std of stimulus to reproduce expected firing rate and CV for the neuron model. 

Reset threshold is defined as the axonal voltage 2ms after the spike detection voltage at the constant input that generates expected firing rate. First temporarily set reset threshold slightly larger than spike detection voltage to determine the constant input. Then with the constant input to find final reset threshold.

In ```~/Code_git/Paramters```, param_step1_runjobs.py calls param_step1_runme.py to find the constant input that about to trigger spikes and the constant input that generates 5Hz firing rate. To find targer stimuli, we set the upper bound and lower bound of the stimuli by hand, and use middle point searching method. firingonset.py in ```~/Code_git/scripts``` contains the function that implements this searching method. When the upper bound and lower bound are close enough, we assume the parameter searching is precise enough. The programme will stop and return the constant input value and final reset threshold for later simulation.
    
To find target mean and std of stimulus, param_step2_runjobs.py calls param_step2_runme.py for parameter searching. In this step, it picks 200 mean values between zero and the constant input of 5Hz firing, and uses midde point searching method to find correponding std to generate 5Hz firing. Determinestd.py in ```~/Code_git/scripts``` provides the function for std searching. param_step3.py summarizes the data. The mean and std that reproduce expected CV are determined by hand from the scatter plots of mean-std and mean-CV relation. Mean and std values are written in the txt file IparamTable.txt in ```~/Code_git/Models/Brette```.
    
## 4. Calculate linear response curves.

Linear response curves of Brette model is calculated by Fourier transform of spike triggered average (STA) divided by power spetral density of stochastic stimulus. In ```~/Code_git/runjobs```, runjobs.py calls runme.py to generate 400 pieces of STA data for given neuron model and stochastic stimulus. Each piece of STA data is an average of about 5000 pieces of stimulus centered at their spike times. Final STA for linear response curve calculation is an average of these 400 pieces of STA data. addparam.py in ```~/Code_git/scripts``` provides the function for loading parameters from IparamTable.txt.

runjobs_desktop.py and runme_desktop.py provides a desktop version of the code. With these two script, one can generate a small fraction of STA data and obtain a preliminary linear response curve.

transferit.py in ```~/Code_git/transferit``` provides function STA_average for averaging STA data and function gain for calculating linear response curve. STA_average is also used for averaging random STA sampling in bootstrapping. In function gain, STA is first suppressed to zero at its two ends before Fourier transform. For Fourier transform, the STA is cut from the middle and attaches its two ends.  

## 5. Bootstrapping confidence interval and null hypothesis test.

To calculate bootstrapping confidence interval, bootstrapping_runjobs.py in ```~/Code_git/transferit/``` calls bootstrapping runme. In each job, it randomly samples 400 pieces of STA data with replacement and averages them to get a new STA. Linear response curves are calculated with new STAs. There are 1000 curves generated in total. Bootstrapping boundaries are the upper bound and lower bound of middle 95 percent of these curves. bootstrapping_step2.py finds the boundary curves and writes them into the linear response curve data file.

To calculate null hypothesis test curve, nullhypothesis_runjobs.py calls in ```~/Code_git/transferit/``` nullhypothesis_runme.py. In each job, it reproduces the stimuli and load corresponding spike time lists. Adding a random number to each spike time list shuffles spike time. STA data are calculated with the stimuli and new spike time lists. nullhypothesis_step2_runjobs.py calls nullhypothesis_step2_runme.py to calculate linear response curves with these STA data. nullhypothesis_step3.py takes the 95 percent upper bound of these curves as the final null hypothesis test curve and writes it into the linear response curve data file.



To calculate the linear response curves of Brette's model with high voltage sensitivity, change the sodium activation parameter k_{a} from 6mV to 0.1mV in NaBrette_point.mod and Neuron.hoc, then compile the mod files. For the neuron model with a small soma, change the soma length and diameter from 50um to 10um in Neuron.hoc.
