import numpy as np
import functions as f
import matplotlib.pyplot as plt
import os


"""----------------------------VIDEO GENERATION------------------------------"""
memorized_patterns = f.generate_patterns(80, 1000)
perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 200)

W= f.hebbian_weights(memorized_patterns)

H = f.dynamics_async(perturbes_pattern.copy(),W, 20000,3000)
print( (memorized_patterns[2] == H[-1]).all() )

memorized_patterns = f.generate_patterns(50, 2500)
memorized_patterns[2]= f.generate_initial_checkerboard().flatten()
perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 1000)

W= f.hebbian_weights(memorized_patterns)

H = f.dynamics_async(perturbes_pattern.copy(),W, 20000,3000)
print( (memorized_patterns[2] == H[-1]).all() )
outpath = os.getcwd()+"/output/hebbian_dynamics_async.mp4"
f.save_video(H,outpath)


"""----------------------------ENERGY FUNCTIONS------------------------------"""

memorized_patterns = f.generate_patterns(50, 2500)
perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 1000)

W_h = f.hebbian_weights(memorized_patterns)
#W_s = f.storkey_weights(memorized_patterns)

history_h = f.dynamics(perturbes_pattern, W_h, 20)
#history_s = f.dynamics(W_s, perturbes_pattern, 20)

history_async_h = f.dynamics_async(perturbes_pattern, W_h, 30000, 10000)
#history_async_s = f.dynamics_async(W_s, perturbes_pattern, 30000, 10000)

plt.figure

plt.subplot(121) 
plt.title('Hebbian weigths and update')
plt.plot(f.plot_energy(history_h,W_h).keys() ,f.plot_energy(history_h,W_h).values())

plt.subplot(122) 
plt.title('Hebbian weigths and update_async')
plt.plot(f.plot_energy(history_async_h,W_h).keys(), f.plot_energy(history_async_h,W_h).values())
""" 
plt.subplot(213) 
plt.title('Storkey weigths and update')
plt.plot(f.plot_energy(history_s,W_s).keys(), f.plot_energy(history_s,W_s).values())

plt.subplot(224) 
plt.title('Storkey weigths and update_async')
plt.plot(f.plot_energy(history_async_s,W_s).keys(), f.plot_energy(history_async_s,W_s).values())
"""

plt.show()

