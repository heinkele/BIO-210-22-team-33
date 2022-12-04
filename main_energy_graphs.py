import numpy as np
import functions as f
import matplotlib.pyplot as plt
import os


def main_energy_graphs():
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


if __name__ == '__main_energy_graphs__':
    main_energy_graphs()
