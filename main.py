import numpy as np
import functions as f
import experiment as e
import matplotlib.pyplot as plt
import pandas as pd
from os import getcwd
from math import log, sqrt




"""----------------------------VIDEO GENERATION------------------------------


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

    """"""----------------------------ENERGY FUNCTIONS------------------------------""""""

    memorized_patterns = f.generate_patterns(50, 2500)
    perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 1000)

    W_h = f.hebbian_weights(memorized_patterns)
    W_s = f.storkey_weights(memorized_patterns)"""
"""
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
"""

"""-------------------------------------EXPERIMENT------------------------------------"""

def main():
    sizes=[10,18]  # 34, 63, 116, 215, 397, 733, 1354, 2500
    results_hebbian=[]
    results_storkey=[]
    hebbian_plots = plt.figure()
    storkey_plots = plt.figure() 
    nb = 0

    for i in range (len(sizes)):
        nb+=1
        n = sizes[i]
        c_n_hebbian = n/(2*log(n, 10))  #log base 10
        c_n_storkey = n/(sqrt(2*log(n, 10)))
        num_patterns_hebbian = np.linspace(0.5 * c_n_hebbian, 2 * c_n_hebbian, 10).astype(int)
        num_patterns_storkey = np.linspace(0.5 * c_n_storkey, 2 * c_n_storkey, 10).astype(int)

        for j in range (10):
            results_hebbian.append(e.experiment(sizes[i], num_patterns_hebbian[j], "hebbian",int(0.2*sizes[i])))
            results_storkey.append(e.experiment(sizes[i], num_patterns_storkey[j], "storkey", int(0.2*sizes[i])))

        df_hebbian = pd.DataFrame(results_hebbian)
        df_storkey = pd.DataFrame(results_storkey)

        # Save dataframe as an hdf5 file
        string = 'summary'+str(n)+'.hdf5'
        outpath = getcwd()+"/summary/hebbian/"+string
        df_hebbian.to_hdf(outpath, key='df_hebbian')
        outpath = getcwd()+"/summary/storkey/"+string
        df_storkey.to_hdf(outpath, key='df_storkey')

        df_hebbian = hebbian_plots.add_subplot(3,4,nb) #numbers of rows and columns 3x4
        plt.plot(df_hebbian.num_patterns, df_hebbian.match_frac)  #unrecognisable keys when plotting !!!!
        df_storkey = storkey_plots.add_subplot(3,4,nb)
        plt.plot(df_storkey.num_patterns, df_storkey.match_frac)

        # Additionally you can let pandas print the table in markdown format for easy pasting!
        print(df_hebbian.to_markdown())
        print(df_storkey.to_markdown())

    # Create a pandas DataFrame from your results dictionary
    plt.show()
 
if __name__ == '__main__':
    main()