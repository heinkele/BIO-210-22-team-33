# Summary of the Hopfield Projet, team 33, BIO-210 :  

## Brief introduction : 

This project implements an iterative process that allows us, by using the Hopfield network model, to retrieve a stored (memorised) pattern from a collection of patterns. 

## 1. Capacity of the Hopfiled network 

An important feature of a Hopfield network is the storage capacity. This corresponds to the number of patterns that our model can store : 
The network is said to have stored a pattern if, when presented with a perturbed version of such pattern, the dynamical system converges to the original one. 

In order to test the capacity of the network, we considered 10 networks of size ranging from 10 to 2500 with logarithmically arranged neuron numbers. 

`(sizes=[10, 18, 34, 63, 116, 215, 397, 733, 1354, 2500])`

We then ran 10 trials, changing the number of patterns each time, for each network size by running the dynamical system varying the initial pattern. We applied a perturbation by changing 20% of the values of each base pattern. We then looked at how many patterns converged back to the original one, in order to compute the fraction of retrieved patterns. We have therefore a total of 200 experiments. 

After running all the experiments, we obtained the following results : 

![Capacity plots](summary/plots/capacity_plots.png "Capacity plots")

In a table format : 


*You will be able to find all our results in hdf5 format in the summary folder.*



## 2. Robustness of the Network 

After testing the capacity of the Network, we want to test its robustness by doing the same experiment as before but with an increasing percent of pertubations (increasing by 5% at each iteration). To do so, we used the same sizes as previously and a pattern containing t=2 patterns each time. Our goal is to obtain the percent of perturbations at which the patterns stop converging more than 10% of the time, i.e returns a convergence below 90%. 

After runing the experiment, we obtain the following tables : 

Hebbian's robustness table : 

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


Storkey's robustness table:

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

![Robustness plots](summary/plots/robustness_plots.png "Robustness plots")

We can see that we obtain a critical percent of perturbations around 39% using the Hebbian rule and 39% when using the Storkey rule. We can't distinguish a major difference between the two rules in this case. As the perturbations are random, the percentage varies a little bit between each trial.

*You will be able to find all our results in hdf5 format in the summary folder.*



## 3. Image retrieval examples 


