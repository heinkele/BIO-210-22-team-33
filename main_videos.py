import numpy as np
import functions as f
import matplotlib.pyplot as plt
import os


def main_videos():
    memorized_patterns = f.generate_patterns(50, 2500)
    memorized_patterns[2] = f.generate_initial_checkerboard().flatten()
    perturbes_pattern = f.perturb_pattern(memorized_patterns[2], 1000)

    W_h = f.hebbian_weights(memorized_patterns)
    W_s = f.storkey_weights(memorized_patterns)

    H_async = f.dynamics_async(perturbes_pattern.copy(), W_h, 20000, 3000)
    H_dyn = f.dynamics(perturbes_pattern.copy(), W_h, 20000)

    S_async = f.dynamics_async(perturbes_pattern.copy(), W_s, 20000, 3000)
    S_dyn = f.dynamics(perturbes_pattern.copy(), W_s, 20000)

    outpath = os.getcwd()+"/output/hebbian_dynamics_async.mp4"
    f.save_video(H_async, outpath)

    outpath = os.getcwd()+"/output/hebbian_dynamics.mp4"
    f.save_video(H_dyn, outpath)

    outpath = os.getcwd()+"/output/storkey_dynamics_async.mp4"
    f.save_video(S_async, outpath)

    outpath = os.getcwd()+"/output/storkey_dynamics.mp4"
    f.save_video(S_dyn, outpath)


if __name__ == '__main_videos__':
    main_videos()
