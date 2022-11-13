import numpy as np
import functions as f

memorized_patterns = f.generate_patterns(3,10)

print("memorized pattern :", memorized_patterns[2])

# our chosen pattern is the 2nd line
perturbed_pattern = f.perturb_pattern2(memorized_patterns[2],4)

print ("perturb pattern :", perturbed_pattern)



W = f.hebbian_weights(memorized_patterns)


dynamic_test = f.dynamics(perturbed_pattern,W,20)
if ((dynamic_test==memorized_patterns[2]).all()):
    print ("Vous etes trop forts")

"""async_dynamic_test = f.dynamics_async(perturbed_pattern,W,20000,3000)
if ((async_dynamic_test==memorized_patterns[2]).all()):
    print ("Vous etes trop forts")
"""

W = f.storkey_weights(memorized_patterns)




f.generate_checkerboard()

memorized_patterns = f.generate_patterns(100,2500)
memorized_patterns[2] = f.flatten_checkerboard(f.generate_initial_checkerboard())
perturbed_pattern = f.perturb_pattern(memorized_patterns[2],1000)
W = f.hebbian_weights(memorized_patterns)
dynamic_test = f.dynamics(perturbed_pattern,W,20)

if ((dynamic_test==memorized_patterns[2]).all()):
    print ("Vous etes trop forts")

async_dynamic_test = f.dynamics_async(perturbed_pattern,W,20000,3000)
if ((async_dynamic_test==memorized_patterns[2]).all()):
    print ("Vous etes trop forts")
    
