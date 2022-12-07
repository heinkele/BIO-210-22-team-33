import numpy as np
import functions as f
import matplotlib.pyplot as plt
import Hopfield_network as h
from os import getcwd

"""


""""""----------------------------VIDEO GENERATION------------------------------"""""""


def main():
    memorized_patterns = f.generate_patterns(50, 2500)
    memorized_patterns[2] = f.generate_initial_checkerboard().flatten()
    perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 1000)

    W_h = f.hebbian_weights(memorized_patterns)

    W_s = f.storkey_weights(memorized_patterns)

    H_async = f.dynamics_async(perturbes_pattern.copy(), W_h, 20000, 3000)
    H_dyn = f.dynamics(perturbes_pattern.copy(), W_h, 20000)

    S_async = f.dynamics_async(perturbes_pattern.copy(), W_s, 20000, 3000)
    S_dyn = f.dynamics(perturbes_pattern.copy(), W_s, 20000)

    outpath = getcwd()+"/output/hebbian_dynamics_async.mp4"
    f.save_video(H_async, outpath)

    outpath = getcwd()+"/output/hebbian_dynamics.mp4"
    f.save_video(H_dyn, outpath)

    outpath = getcwd()+"/output/storkey_dynamics_async.mp4"
    f.save_video(S_async, outpath)

    outpath = getcwd()+"/output/storkey_dynamics.mp4"
    f.save_video(S_dyn, outpath)

    """"""----------------------------ENERGY FUNCTIONS------------------------------"""""""

    memorized_patterns = f.generate_patterns(50, 2500)
    perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 1000)

    W_h = f.hebbian_weights(memorized_patterns)
    W_s = f.storkey_weights(memorized_patterns)

    history_h = f.dynamics(perturbes_pattern, W_h, 20)
    history_s = f.dynamics(perturbes_pattern, W_s, 20)

    history_async_h = f.dynamics_async(perturbes_pattern, W_h, 30000, 10000)
    history_async_s = f.dynamics_async(perturbes_pattern, W_s, 30000, 10000)

    plt.figure

    plt.subplot(221)
    plt.title('Hebbian weigths and update')
    plt.plot(f.plot_energy(history_h, W_h).keys(),
             f.plot_energy(history_h, W_h).values())

    plt.subplot(222)
    plt.title('Hebbian weigths and update_async')
    plt.plot(f.plot_energy(history_async_h, W_h).keys(),
             f.plot_energy(history_async_h, W_h).values())

    plt.subplot(223)
    plt.title('Storkey weigths and update')
    plt.plot(f.plot_energy(history_s, W_s).keys(),
             f.plot_energy(history_s, W_s).values())

    plt.subplot(224)
    plt.title('Storkey weigths and update_async')
    plt.plot(f.plot_energy(history_async_s, W_s).keys(),
             f.plot_energy(history_async_s, W_s).values())

    plt.show()


if __name__ == '__main__':
    main()


""" 


def main():

    memorized_patterns = h.Patterns(50, 2500)
    memorized_patterns = memorized_patterns.generate_patterns()
    
    memorized_patterns[2] = h.generate_initial_checkerboard().flatten()   
    
    perturbes_pattern = memorized_patterns.perturb_patterns(memorized_patterns[2], 1000)
    print(perturbes_pattern)

    W = h.HopfieldNetwork(memorized_patterns, "hebbian")

    saver = h.DataSaver()

    W_async = W.dynamics_async(perturbes_pattern.copy(), saver, 20000, 3000)

    outpath = getcwd()+"/output/hebbian_dynamics_async.mp4"
    W.plot_energy()
    h.save_video(W_async, outpath)

if __name__ == '__main__':
    main()
