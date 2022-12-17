import numpy as np
import functions as f
import experiment as e
import robustness as r
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
"""
def main():
    sizes=[10,18,34, 63, 116, 215, 397, 733, 1354, 2500]
    results_hebbian=[]
    results_storkey=[]
    hebbian_plot = []
    storkey_plot = []
    df_hebbian_list = []
    df_storkey_list = []

    for i in range (len(sizes)):
        n = sizes[i]
        c_n_hebbian = n/(2*log(n, 10))  #log base 10
        c_n_storkey = n/(sqrt(2*log(n, 10)))
        num_patterns_hebbian = np.linspace(0.5 * c_n_hebbian, 2 * c_n_hebbian, 10).astype(int)
        num_patterns_storkey = np.linspace(0.5 * c_n_storkey, 2 * c_n_storkey, 10).astype(int)

        for j in range (10):
            exp_hebbian = e.experiment(sizes[i], num_patterns_hebbian[j], "hebbian",int(0.2*sizes[i]))
            exp_storkey = e.experiment(sizes[i], num_patterns_hebbian[j], "storkey",int(0.2*sizes[i]))
            results_hebbian.append(exp_hebbian)
            results_storkey.append(exp_storkey)
            hebbian_plot.append(exp_hebbian)
            storkey_plot.append(exp_storkey)

        df_hebbian = pd.DataFrame(hebbian_plot)
        df_storkey = pd.DataFrame(storkey_plot)
        df_hebbian_list.append(df_hebbian)
        df_storkey_list.append(df_storkey)
        hebbian_plot.clear()
        storkey_plot.clear()

        fig, axes = plt.subplots(nrows=2, ncols=5)

        for k in range(len(df_hebbian_list)):
            if k < 5 :
                df_hebbian_list[k].plot(x = 'num_patterns', y = 'match_frac', ax= axes[0,k], label = 'hebbian')
                df_storkey_list[k].plot(x = 'num_patterns', y = 'match_frac', ax= axes[0,k], label = 'storkey')
            else:
                df_hebbian_list[k].plot(x = 'num_patterns', y = 'match_frac', ax= axes[1,k%5], label = 'hebbian')
                df_storkey_list[k].plot(x = 'num_patterns', y = 'match_frac', ax= axes[1,k%5], label = 'storkey')
        
        plt.show()

        df_hebbian = pd.DataFrame(results_hebbian)
        df_storkey = pd.DataFrame(results_storkey)

        # Save dataframe as an hdf5 file
        outpath = getcwd()+"/summary/hebbian_summary.hdf5"
        df_hebbian.to_hdf(outpath, key='df_hebbian')
        outpath = getcwd()+"/summary/storkey_summary.hdf5"
        df_storkey.to_hdf(outpath, key='df_storkey')

        print(df_hebbian.to_markdown())
        print(df_storkey.to_markdown())
"""
def main():
    sizes=[10,18,34, 63, 116, 215, 397, 733, 1354, 2500]
    convergence_percentage_hebbian_list = []
    convergence_percentage_storkey_list = []
    percentage = 0.15

    while percentage <= 0.95 :
        percentage += 0.05
        convergence_percentage_hebbian_dict = {"perturb_percentage": percentage, "match_percentage" : r.robustness(sizes, "hebbian", percentage)}
        convergence_percentage_storkey_dict = {"perturb_percentage": percentage, "match_percentage" : r.robustness(sizes, "storkey", percentage)}
        convergence_percentage_hebbian_list.append(convergence_percentage_hebbian_dict)
        convergence_percentage_storkey_list.append(convergence_percentage_storkey_dict)

    df_hebbian = pd.DataFrame(convergence_percentage_hebbian_list)
    df_storkey = pd.DataFrame(convergence_percentage_storkey_list)

     # Save dataframe as an hdf5 file
    outpath = getcwd()+"/summary/hebbian_robustness.hdf5"
    df_hebbian.to_hdf(outpath, key='df_hebbian')
    outpath = getcwd()+"/summary/storkey_robustness.hdf5"
    df_storkey.to_hdf(outpath, key='df_storkey')

    print(df_hebbian.to_markdown())
    print(df_storkey.to_markdown())

    df_hebbian.plot(x = 'perturb_percentage', y = 'match_percentage', label = 'hebbian', color = 'blue')
    plt.show()
    df_storkey.plot(x = 'perturb_percentage', y = 'match_percentage', label = 'storkey', color = 'orange')
    plt.show()


 
if __name__ == '__main__':
    main()