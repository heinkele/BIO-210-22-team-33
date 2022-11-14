import functions as f
import numpy as np

def test_generate_patterns ():
    # valeurs generiques

    # cas limite
    return


def test_hebbian_weights():
    assert np.allclose(f.hebbian_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]))

def test_storkey_weights():
    assert np.allclose(f.storkey_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[1.125, 0.25, -0.25, -0.5], [0.25, 0.625, -1, 0.25], [-0.25, -1, 0.625, -0.25], [-0.5, 0.25, -0.25, 1.125]]))