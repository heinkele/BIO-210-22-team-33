# Summary of the Hopfield Projet, team 33, BIO-210 :  

## Brief introduction : 

This project implements an iterative process that allows us, using the Hopfield network model, to retreive a stored (memorised) pattern from a collection of patterns. 

## 1. Capacity of the Hopfiled network 

An important feature of a Hopfield network is the storage capacity, which means how many patterns can the model store : 
*The network is said to have stored a pattern if, when presented with a perturbed version of such pattern, the dynamical system converges to the original one* 

In order to test the capacity of the network, we consider 10 networks of size ranging from 10 to 2500 with logarithmically arranged neuron numbers. 

`(sizes=[10, 18, 34, 63, 116, 215, 397, 733, 1354, 2500])`

We than run 10 trials, changing the number of patterns each time, for each network size by running the dynamical system varying the initial patern and the perturbation (we apply a perturbation by changing 20% of the values of each base pattern). We look at how many patterns converge to the original one, in order to compute the fraction of retrieved patterns. We have therefore a total of 200 experiments. 

After running this experiment, we obtain the following graphs : 

*insert picture or file*

Followed by the following table : 

*insert picture or file*

## 2. Robustness of the Network 

After testing the capacity of the Network, we test its robustness by doing the same experiment as before but with an increasing purcent of pertubation (increasing 5% by 5%). To do so, we use the same sizes as before and a pattern containing two patterns each time. Our aim is to obtain the percent of perturbations that returns a convergence bellow 90%. 

After runing the experiment, we obtain the following graphs : 

*insert picture or file*

Followed by the following tables : 

Hebbian robustness table : 

|    |   perturb_percentage |   match_percentage |
|---:|---------------------:|-------------------:|
|  0 |                 0.2  |               0.94 |
|  1 |                 0.25 |               0.98 |
|  2 |                 0.3  |               0.95 |
|  3 |                 0.35 |               0.95 |
|  4 |                 0.4  |               0.9  |
|  5 |                 0.45 |               0.67 |
|  6 |                 0.5  |               0.02 |
|  7 |                 0.55 |               0    |
|  8 |                 0.6  |               0    |
|  9 |                 0.65 |               0    |
| 10 |                 0.7  |               0    |
| 11 |                 0.75 |               0    |
| 12 |                 0.8  |               0    |
| 13 |                 0.85 |               0    |
| 14 |                 0.9  |               0    |
| 15 |                 0.95 |               0    |


Storkey robustness table:

|    |   perturb_percentage |   match_percentage |
|---:|---------------------:|-------------------:|
|  0 |                 0.2  |               1    |
|  1 |                 0.25 |               0.98 |
|  2 |                 0.3  |               0.98 |
|  3 |                 0.35 |               0.93 |
|  4 |                 0.4  |               0.87 |
|  5 |                 0.45 |               0.71 |
|  6 |                 0.5  |               0.08 |
|  7 |                 0.55 |               0    |
|  8 |                 0.6  |               0    |
|  9 |                 0.65 |               0    |
| 10 |                 0.7  |               0    |
| 11 |                 0.75 |               0    |
| 12 |                 0.8  |               0    |
| 13 |                 0.85 |               0    |
| 14 |                 0.9  |               0    |
| 15 |                 0.95 |               0    |


We can see that we obtain a critical percent of perturbations of : 25-30% with the Hebbian calculations and 30-35% with the Sorkey calculations. As the perturbations are random, the penrcentage varies a little bit between each trial.   

## 3. Image retrival examples 


