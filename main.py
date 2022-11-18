import numpy as np
import functions as f
import matplotlib.pyplot as plt


memorized_patterns = f.generate_patterns(50, 2500)
perturbes_pattern = f.perturb_pattern(memorized_patterns[5], 1000)

W_h = f.hebbian_weights(memorized_patterns)
W_s = f.storkey_weights(memorized_patterns)


history_h = f.dynamics(W_h, perturbes_pattern, 20)
history_s = f.dynamics(W_s, perturbes_pattern, 20)
history_async_h = f.dynamics_async(W_h, perturbes_pattern, 30000, 10000)
history_async_s = f.dynamics_async(W_s, perturbes_pattern, 30000, 10000)

#drawing of the 4 plots
plt.figure

plt.subplot(141) 
plt.title('Hebbian weigths and update')
plt.scatter(history_h)

plt.subplot(142) 
plt.title('Hebbian weigths and update_async')
plt.scatter(history_async_h)

plt.subplot(243)
plt.title('Storkey weigths and update')
plt.scatter(history_s)

plt.subplot(244)
plt.title('Storkey weigths and update_async')
plt.scatter(history_async_s)

plt.show()





"""

memorized_patterns = f.generate_patterns(3,50)
print("memorized pattern :", memorized_patterns[2]) # our chosen pattern is the 2nd line

perturbed_pattern = f.perturb_pattern(memorized_patterns[2],10)
print ("perturbed pattern :", perturbed_pattern)

W = f.hebbian_weights(memorized_patterns)
print ("W :", W)

dynamic_test = f.dynamics(perturbed_pattern,W,20)
if ((dynamic_test==memorized_patterns[2]).all()):
    print ("Vous etes trop forts")

#W = f.storkey_weights(memorized_patterns)

#f.energy(perturbed_pattern, W)



async_dynamic_test = f.dynamics_async(perturbed_pattern,W,20000,3000)
if ((async_dynamic_test==memorized_patterns[2]).all()):
    print ("Vous etes trop forts")





f.generate_initial_checkerboard()

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



print ( f.generate_initial_checkerboard())

"""