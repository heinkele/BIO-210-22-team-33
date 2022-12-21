import numpy as np
import functions as f
import experiment as e
import robustness as r
import matplotlib.pyplot as plt
import pandas as pd
from os import getcwd


video_generation = False
energy_functions = False
capacity_analysis = True
robustness_testing = False


#--------------------------VIDEO GENERATION-----------------------------


def main():
    if video_generation == True :
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



#----------------------------ENERGY FUNCTIONS------------------------------

    if video_generation == True :
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



#-------------------------------------CAPACITY ANALYSIS------------------------------------

    if capacity_analysis == True : 
        sizes = [10, 18, 34, 63]
        #, 116, 215, 397, 733, 1354, 2500]
        hebbian_plot = []
        storkey_plot = []
        df_hebbian_list = []
        df_storkey_list = []

        list_match_hebbian = []
        list_match_storkey = []

        for i in range(len(sizes)): #iteration on all the sizes
            n = sizes[i]
            c_n_hebbian = e.c(n, 'hebbian')
            c_n_storkey = e.c(n, 'storkey')
            num_patterns_hebbian = np.linspace(
                0.5 * c_n_hebbian, 2 * c_n_hebbian, 10).astype(int)
            num_patterns_storkey = np.linspace(
                0.5 * c_n_storkey, 2 * c_n_storkey, 10).astype(int)

            last_one_hebbian = 0
            last_one_storkey = 0

            for j in range(10): #iteration on all the different num patterns per size
                exp_hebbian = e.experiment(
                    sizes[i], num_patterns_hebbian[j], "hebbian", int(0.2*sizes[i]))
                exp_storkey = e.experiment(
                    sizes[i], num_patterns_storkey[j], "storkey", int(0.2*sizes[i]))
                hebbian_plot.append(exp_hebbian)
                storkey_plot.append(exp_storkey)

                if (exp_hebbian["match_frac"] >= 0.9):
                    last_one_hebbian = exp_hebbian["num_patterns"]
                if (exp_storkey["match_frac"] >= 0.9):
                    last_one_storkey = exp_storkey["num_patterns"]

            list_match_hebbian.append(last_one_hebbian)
            list_match_storkey.append(last_one_storkey)

            df_hebbian = pd.DataFrame(hebbian_plot)
            df_storkey = pd.DataFrame(storkey_plot)

            # Save dataframe as an hdf5 file
            outpath = getcwd()+"/summary/hebbian_summary" + str(sizes[i]) + ".hdf5"
            df_hebbian.to_hdf(outpath, key='df_hebbian')
            outpath = getcwd()+"/summary/storkey_summary" + str(sizes[i]) + ".hdf5"
            df_storkey.to_hdf(outpath, key='df_storkey')
            print(df_hebbian.to_markdown())
            print(df_storkey.to_markdown())

            df_hebbian_list.append(df_hebbian)
            df_storkey_list.append(df_storkey)
            hebbian_plot.clear()
            storkey_plot.clear()

            fig, axes = plt.subplots(nrows=2, ncols=5)

            for k in range(len(df_hebbian_list)): #iteration to realize all the subplots
                plt.subplot(5, 2, k+1)
                plt.plot(df_hebbian_list[k]['num_patterns'],
                        df_hebbian_list[k]['match_frac'], label='hebbian')
                plt.legend()
                plt.subplot(5, 2, k+1)
                plt.plot(df_storkey_list[k]['num_patterns'],
                        df_storkey_list[k]['match_frac'], label='storkey')
                plt.legend()
                plt.xlabel("num_patterns")
                plt.ylabel("match_frac")
                plt.ylim(0, 1)

            plt.show()

        plt.plot(sizes, list_match_hebbian,
                label='empirical_hebbian', color='blue')
        plt.plot(sizes, list_match_storkey,
                label='empirical_storkey', color='orange')
        plt.plot(sizes, e.c(sizes, 'hebbian'),
                label='theoretical_hebbian', color='blue', alpha=0.5)
        plt.plot(sizes, e.c(sizes, 'storkey'),
                label='theoretical_storkey', color='orange', alpha=0.5)
        plt.legend()
        plt.xlabel('sizes')
        plt.ylabel('num_pattern')

        plt.show()


#-------------------------------------ROBUSTNESS TESTING------------------------------------


    if robustness_testing == True :
        sizes = [10, 18, 34, 63, 116, 215, 397, 733, 1354, 2500]
        convergence_percentage_hebbian_list = []
        convergence_percentage_storkey_list = []
        percentage = 0.15

        while percentage <= 0.95:
            percentage += 0.05
            convergence_percentage_hebbian_dict = {
                "perturb_percentage": percentage, "match_percentage": r.robustness(sizes, "hebbian", percentage)}
            convergence_percentage_storkey_dict = {
                "perturb_percentage": percentage, "match_percentage": r.robustness(sizes, "storkey", percentage)}
            convergence_percentage_hebbian_list.append(
                convergence_percentage_hebbian_dict)
            convergence_percentage_storkey_list.append(
                convergence_percentage_storkey_dict)

        df_hebbian = pd.DataFrame(convergence_percentage_hebbian_list)
        df_storkey = pd.DataFrame(convergence_percentage_storkey_list)

        # Save dataframe as an hdf5 file
        outpath = getcwd()+"/summary/hebbian_robustness.hdf5"
        df_hebbian.to_hdf(outpath, key='df_hebbian')
        outpath = getcwd()+"/summary/storkey_robustness.hdf5"
        df_storkey.to_hdf(outpath, key='df_storkey')

        print(df_hebbian.to_markdown())
        print(df_storkey.to_markdown())

        df_hebbian.plot(x='perturb_percentage', y='match_percentage',
                        label='hebbian', color='blue')
        plt.show()
        df_storkey.plot(x='perturb_percentage', y='match_percentage',
                        label='storkey', color='orange')
        plt.show()


if __name__ == '__main__':
    main()
