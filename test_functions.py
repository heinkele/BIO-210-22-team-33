import functions as f
import numpy as np
from os import getcwd
from os import path


def test_generate_patterns():
    M = f.generate_patterns(3, 4)
    assert M.shape[0] == 3  # size tests
    assert M.shape[1] == 4
    assert all(m in M for m in [1, -1])  # value tests


def test_perturb_pattern():
    t = list(f.perturb_pattern(np.ones(50), 20))
    assert t.count(-1) == 20
    assert all(m in t for m in [1, -1])  # value tests


def test_hebbian_weights(benchmark):
    assert np.allclose(f.hebbian_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([
                       [0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]))
    #hebbian_weight = f.hebbian_weights(f.generate_patterns(3,4))
    hebbian_weight = benchmark.pedantic(f.hebbian_weights, args=(
        f.generate_patterns(50, 2500),), rounds=5, iterations=1)

    assert np.shape(hebbian_weight)[0] == 2500
    assert np.shape(hebbian_weight)[0] == np.shape(hebbian_weight)[1]
    assert [hebbian_weight <= 1] and [hebbian_weight >= -1]
    assert (np.diag(hebbian_weight) == 0).all()


def test_update(benchmark):
    #assert np.allclose(f.update(np.array([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]), ([-1, 1, 1, 1])), ([-1, -1, -1, 1]))
    patterns = f.generate_patterns(50, 2500)
    update = benchmark.pedantic(f.update, args=(f.perturb_pattern(
        patterns[1], 1000), f.hebbian_weights(patterns)), rounds=5, iterations=1)

    assert np.allclose(f.update(np.array([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3],
                       [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]), ([-1, 1, 1, 1])), ([-1, -1, -1, 1]))


def test_update_async(benchmark):
    memorized_patterns = f.generate_patterns(2, 10)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[1], 5)
    W_h = f.hebbian_weights(memorized_patterns)
    updated_pattern = f.update_async(perturbed_pattern, W_h)
    compar = list(perturbed_pattern - updated_pattern)
    assert (compar.count(0) == (len(updated_pattern)-1) and (compar.count(2) == 1 or compar.count(-2) == 1)
            ) or (compar.count(0) == len(updated_pattern))  # only one element has changed or nothing changed

    patterns = f.generate_patterns(50, 2500)
    update_async = benchmark.pedantic(f.update, args=(f.perturb_pattern(
        patterns[1], 1000), f.hebbian_weights(patterns)), rounds=5, iterations=1)


def test_dynamics(benchmark):
    memorized_patterns = f.generate_patterns(8, 1000)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[2], 200)
    W = f.hebbian_weights(memorized_patterns)
    history = f.dynamics(perturbed_pattern, W, 20)
    patterns = f.generate_patterns(50, 2500)
    dynamics = benchmark.pedantic(f.dynamics, args=(f.perturb_pattern(
        patterns[1], 1000), f.hebbian_weights(patterns), 20), rounds=5, iterations=1)

    assert np.shape(history)[0] <= 20  # max iteration
    if np.shape(history)[0] < 20:
        assert (history[-1] == history[-2]).all()  # convergence


def test_dynamic_async(benchmark):
    memorized_patterns = f.generate_patterns(8, 1000)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[2], 200)
    W = f.hebbian_weights(memorized_patterns)
    history = f.dynamics_async(perturbed_pattern, W, 20000, 3000)
    patterns = f.generate_patterns(50, 2500)
    dynamics_async = benchmark.pedantic(f.dynamics_async, args=(f.perturb_pattern(
        patterns[1], 1000), f.hebbian_weights(patterns), 30000, 10000), rounds=5, iterations=1)

    # max iteration 1/1000 elements in history
    assert np.shape(history)[0] <= 20
    if np.shape(history)[0] < 20:
        assert (history[-1] == history[-2]).all and (history[-2]
                                                     == history[-3]).all()  # convergence


def test_storkey_weights(benchmark):
    # generic values
    assert np.allclose(f.storkey_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([
                       [1.125, 0.25, -0.25, -0.5], [0.25, 0.625, -1, 0.25], [-0.25, -1, 0.625, -0.25], [-0.5, 0.25, -0.25, 1.125]]))
    storkey_weight = benchmark.pedantic(f.storkey_weights, args=(
        f.generate_patterns(50, 2500),), rounds=5, iterations=1)
    assert np.shape(storkey_weight)[0] == 2500  # size tests
    assert np.shape(storkey_weight)[0] == np.shape(storkey_weight)[1]


def test_energy(benchmark):
    memorized_patterns = np.array([1, -1])
    W = np.array([[0, 1/3], [1/3, 0]])
    assert f.energy(memorized_patterns, W) == 1/3
    patterns = f.generate_patterns(50, 2500)
    energy = benchmark.pedantic(f.energy, args=(f.perturb_pattern(
        patterns[1], 1000), f.hebbian_weights(patterns)), rounds=5, iterations=1)


def test_generate_initial_checkerboard():
    checkerboard = (np.reshape(
        f.generate_initial_checkerboard(), (-1))).tolist()
    assert checkerboard.count(1.) == 1250
    assert checkerboard.count(-1.) == 1250


def test_pattern_match():
    assert f.pattern_match(
        np.array([[1, -1, 1], [1, 1, 1], [-1, -1, 1]]), np.array([1, 1, 1])) == 1
    assert f.pattern_match(
        np.array([[1, -1, 1], [1, 1, 1], [-1, -1, 1]]), [1, 1, -1]) == None


def test_save_video():
    outpath = getcwd()+"/output/hebbian_dynamics_async.mp4"
    f.save_video(f.generate_patterns(1, 2500), outpath)
    path.exists(outpath)
    # "/Users/mischaluefkens/Desktop/SOFTWARE/BIO-210-22-team-33/output/hebbian_dynamics_async.mp4"
    assert path.exists(outpath) == True


def test_plot_energy():
    memorized_patterns = f.generate_patterns(8, 1000)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[2], 200)
    W = f.hebbian_weights(memorized_patterns)  # same with stokey

    history = f.dynamics(perturbed_pattern, W, 20)
    dict = list(f.plot_energy(history, W).values())
    for i in range(len(dict)-1):
        assert dict[i] >= dict[i+1]  # non-increasing
