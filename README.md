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

# Code Running 
To access the videos of the update, run the file main_videos.py
To access the graphs, run the file main_energy_graphs.py 


# Testing

We use [pytest](https://docs.pytest.org/en/6.2.x/contents.html).


## Pytests

We created unit-tests for the `functions.py` in `test_functions.py`. You can also run the whole test-suite with

```pytest```

## Coverage

You can assess the coverage by running:

```
coverage run -m pytest
coverage report
coverage report html
```
Coverage report html gives you a detailed report. 
