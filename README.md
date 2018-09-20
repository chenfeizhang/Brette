# Python Code for Neuron Model Simulation and Linear Response Function Calculation:

The Python code here simulates a simple multi-compartment model proposed by [Brette 2013](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003338) and calculates its linear response functions which describe the population encoding ability of the neuron model. 

It first provides a procedure to determine the axonal voltages for spike time detection and voltage reset to finish a spike. It also provides a parameter searching procedure to determine mean and std of stochastic stimulus which reproduce expected firing rate and coefficient variation (CV) of iter-spike intervals (ISI) of the neuron model. Thirdly, it implements the methods proposed by [Higgs et al. 2009](http://www.jneurosci.org/content/29/5/1285.long) to calculate the linear response functions of the neuron model which shows the impact of neuron morphology, spike initiation dynamics and stimulus properties on population encoding abilities. In the last part, it provides a procedure for calculating bootstrapping confidence intervals and null hypothesis test curves. This is the code for our [manuscript](https://arxiv.org/abs/1807.00509). 

## 1. How to Get Started

To run the code, we used Python 2.6 complied with NEURON 7.3. Some scripts are run on the cluster. Place the code folder Code_git in home directory, go to directory ~/Code_git/Models/Brette. Compile the mod file with command ```nrnivmodl```. The other two directories Brette_ka01 and Brette_soma10_ka01 contain neuron models with different parameter setup. Compile corresponding mod files before running simulations with these models. 

## 2. Determine Axonal Voltage for Spike Time Dectection

Brette model is a simple multi-compartment model composed of a soma and an axon. Only sodium channels are located at point on the axon for spike generation (AP initiation site). The rest of the neuron model is passive. To finish a spike, it requires to reset the voltage of the whole neuron when the axonal voltage at the AP initiation site reaches some specific value. We call this reset threshold. To determine the spike time, we choose the axonal voltage with the maximum voltage derivative for spike time dectection.

model_simulation.py in ~/Code_git/Parameters provides a function for model simulation and a function for stimulus generation. It also provides self-test code to run model simulation with the following command:

```
~/Code_git/Models/Brette/x86_64/special -python model_simulation.py Brette
```
To determine spike time dectection voltage at the AP initiation site, we first set reset threshold to the reserval potential of sodium channels, which is 60mV. Injecting the soma with a constant stimulus of appropriate size, choose the axonal voltage with the maximum voltage derivative as the spike detection voltage. The stimulus size should be large enough to make axonal voltage pass half-activation voltage of sodium channels, which is -40mV. It also shouldn't be too large to make the voltage larger than the reserval potential. Spike detection voltage is quite insensitive to the constant stimulus amplitude. In fact, the axonal voltages around the spike detection voltage will usually fall in the same time bin during the simulation, which will not affect spike time detection.


## 3. Determine mean and std of stimulus to reproduce expected firing rate and CV for the neuron model. 

Reset threshold is defined as the axonal voltage 2ms after the spike detection voltage at the constant input that generates expected firing rate. First temporarily set reset threshold slightly larger than spike detection voltage to determine the constant input. Then with the constant input to find final reset threshold.

In ~/Code_git/Paramters, param_step1_runjobs.py calls param_step1_runme.py to find the constant input that about to trigger spikes and the constant input that generates 5Hz firing rate. To find targer stimuli, we set the upper bound and lower bound of the stimuli by hand, and use middle point searching method. firingonset.py in ~/Code_git/scripts contains the function that implements this searching method.
    

    
    d. Summarize the mean-std and mean-CV relation with param_step3.py. Find the mean and std that reproduce expected firing rate and CV by hand.
    
## 3. Calculate linear response curves.

    a. Write the simulation parameters in the file IparamTable.txt in ~/Code/Models/Brette.
    
    b. Calculate the STA for linear response curves with the file runjobs.py in ~/Code/runjobs.
    
    c. Calculate the linear response curves with the file transferit.py in ~/Code/transferit. To run this file: ~/Code/Models/Brette/x86_64/special -python transferit.py

4. Bootstrapping confidence interval and null hypothesis test.

    a. Calculate the bootstrapping confidence interval with bootstrapping_runjobs.py. Write the upper bound and lower bound of the confidence intervals into the file of linear response curve with bootstrapping_step2.py.

    b. Calculate the STA with the shuffled spike times with null_hypothesis_runjobs.py. Use these STAs to calculate the linear response curve with nullhypothesis_step2_runjobs.py. Take the 95 percent bound of these curves as the null hypothesis test curve with nullhypothesis_step3.py.

To calculate the linear response curves of Brette's model with high voltage sensitivity, change the sodium activation parameter k_{a} from 6mV to 0.1mV in NaBrette_point.mod and Neuron.hoc, then compile the mod files. For the neuron model with a small soma, change the soma length and diameter from 50um to 10um in Neuron.hoc.
