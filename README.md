# GitHub EPFL-BIO-210-22-team-33

This project's goal is to implement an interative process which allows to retreive one the stored (memorized) patterns starting from the representation of a unknown pattern. 
The Hopfield Network will be used as our model to retrieve the memory. 

# Authors
This project is made by Hugo Heinkele, Mischa Luefkens and Salomé Peyrache under supervision of Kamila Babayeva. 


# Requirements
- Python >= 3.5
- numpy
- matplotlib
- os

You can access our environmental file with those commandes : 
`conda env create -f environment.yml`

You can activate the environment using:
`conda activate hopefiled_network_team33`


# Usage

If you wish to generate the 4 energy graphs (vs time), uncomment the part named `ENERGY FUNCTIONS` in the file main.py and run it with the following command in the terminal :
`python main.py`

This will generate 4 energy graphs combining one of the two different weight calculation systems (hebbian and storkey) and one of the two different update systems (asynchronous or not)

If you wish to visualize the evolution of the convergence with a checkerboard of each 4 systems, uncomment the part named `VIDEO GENERATION` in the file main.py and run it with the following command :
`python main.py`

This will generate 4 videos which aim to converge back to the initial state represented by a checkerboard.

If you wish to run both of the previous commands at once, uncomment both parts and run the file main.py with the following command :
`python main.py`

# Model Analysis 

If you wish to test the capacity of the Hopefild Network, uncomment the part named `CAPACITY ANALYSIS` in the file main.py and run it. 

This will generate 10 graphs of the matching fraction over the number of patterns used and a table of the results. 

If you which to test the robustness of the Hopefiled Network, uncomment the part named `ROBUSTNESS TESTING` in the file main.py and run it

This will generate 2 graphs of the percentage of matching fraction over the percentage of perturbation, and a table of the results.  

You will find more information in the file `Summary.md`


# Testing

We use [pytest](https://docs.pytest.org/en/6.2.x/contents.html).


## Pytests

We created unit-tests for the file `functions.py` in `test_functions.py`. You can also run the whole test-suite with

```pytest```

This command will also run benchmark. 



## Coverage

You can assess the coverage by running:

`coverage run -m pytest`
`coverage report`
`coverage report html`

Coverage report html gives you a detailed report. 
