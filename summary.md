# Summary of the Hopfield Projet, team 33, BIO-210 :  

## Brief introduction : 

This project implements an iterative process that allows us, using the Hopfield network model, to retreive a stored (memorised) pattern from a collection of patterns. 

## 1. Capacity of the Hopfiled network 

An important feature of a Hopfield network is the storage capacity, which means how many patterns can the model store : 
*The network is said to have stored a pattern if, when presented with a perturbed version of such pattern, the dynamical system converges to the original one* 

In order to test the capacity of the network, we consider 10 networks of size ranging from 10 to 2500 with logarithmically arranged neuron numbers. 

`(sizes=[10, 18, 34, 63, 116, 215, 397, 733, 1354, 2500])`

We than run 10 trials, changing the number of patterns each time, for each network size by running the dynamical system varying the initial patern and the perturbation (we apply a perturbation by changing 20% of the values of each base pattern). We look at how many patterns converge to the original one, in order to compute the fraction of retrieved patterns. We have therefore a total of 200 experiments. 

## 2. Robustness of the Network 

## 3. Image retrival examples 
