import functions as f
import numpy as np

def test_generate_patterns ():
    # generic values
    M = f.generate_patterns(3,4)
    assert M.shape[0] == 3  #size tests
    assert M.shape[1] == 4
    assert all(m in M for m in [1, -1]) #value tests
    # exceptions treated in doctests

def test_perturb_pattern():
    # generic values
    t = list(f.perturb_pattern(np.ones(50),20))
    assert t.count(-1) == 20
    # exceptions treated in doctests

""" 
def test_pattern_match():
    hahj

def test_hebbian_weights():
    assert np.allclose(f.hebbian_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]))

def test_update2():
    hahj

def test_update_async():
    hahj

def test_dynamics():
    hahj

def test_dynamics_async():
    hahj

def test_storkey_weights():
    assert np.allclose(f.storkey_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[1.125, 0.25, -0.25, -0.5], [0.25, 0.625, -1, 0.25], [-0.25, -1, 0.625, -0.25], [-0.5, 0.25, -0.25, 1.125]]))

def test_energy():
    hahj

def test_generate_initial_checkerboard():
    hahj

def test_flatten_checkerboard():
    hahj

def test_vector_to_matrix():
    hahj

def test_marix_list():
    hahj

def test_save_video():
    hahj
    
"""