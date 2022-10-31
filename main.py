import numpy as np
import functions as f

memorized_patterns = f.generate_patterns(80,1000)

# our chosen pattern is the 2nd line
perturbed_pattern = f.perturb_pattern(memorized_patterns[2],200)

W = f.hebbian_weights(memorized_patterns)

dynamic_test = f.dynamics(perturbed_pattern,W,20)
if (dynamic_test==memorized_patterns[2]):
    print ("Vous etes trop forts")
