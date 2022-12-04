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

If you wish to generate the 4 energy graphs (vs time), run the file main_energy_graphs.py with the following command in the terminal :
`python main_energy_graphs.py` 
This will generate 4 energy graphs combining one of the two different weight calculation systems (hebbian and storkey) and one of the two different update systems (asynchronous or not)

If you wish to visualize the evolution of the convergence with a checkerboard of each 4 systems, run the file main_videos.py with the following command :
`python main_videos.py`       
This will generate 4 videos which aim to converge back to the initial state represented by a checkerboard.

If you wish to run both of the previous commands at once, run main.py with the following command :
`python main.py`


# Testing

We use [pytest](https://docs.pytest.org/en/6.2.x/contents.html).


## Pytests

We created unit-tests for the `functions.py` in `test_functions.py`. You can also run the whole test-suite with

```pytest```

## Coverage

You can assess the coverage by running:

`coverage run -m pytest`
`coverage report`
`coverage report html`

Coverage report html gives you a detailed report. 
