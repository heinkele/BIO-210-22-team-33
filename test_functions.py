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
    assert all(m in t for m in [1, -1]) #value tests
    # exceptions treated in doctests
""""
--------------------------- HUGO -------------------------------

"""

def test_hebbian_weights():
    # generic values
    assert np.allclose(f.hebbian_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]))
    memorized_patterns = f.generate_patterns(3,4)
    hebbian_weight = f.hebbian_weights(memorized_patterns)
    assert np.shape(hebbian_weight)[0] == 4  
    assert np.shape(hebbian_weight)[0] == np.shape(hebbian_weight)[1]
    for i in range (np.shape(hebbian_weight)[0]):
        for j in range (np.shape(hebbian_weight)[1]):
            assert (hebbian_weight[i][j] <= 1) and (hebbian_weight[i][j] >= -1)
            assert hebbian_weight[i][j] == hebbian_weight[j][i]
            if i==j :
                assert hebbian_weight[i][j] == 0

def test_update():
    assert np.allclose(f.update(np.array([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]]), ([-1, 1, 1, 1])), ([-1, -1, -1, 1]))

def test_dynamics():
    assert np.allclose(f.dynamics(([-1, 1, -1, 1]), [[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]], 20), [[1, 1, -1, 1], [1, 1, -1, 1]])
    memorized_pattern = np.array([1, 1, -1, 1])
    perturbed_pattern = np.array([-1, 1, 1, 1])  #3 perturbations
    hebbian_weight = np.array([[0, 1/3, -1/3, -1/3], [1/3, 0, -1, 1/3], [-1/3, -1, 0, -1/3], [-1/3, 1/3, -1/3, 0]])
    assert np.allclose(f.dynamics(perturbed_pattern, hebbian_weight, 20)[-1], memorized_pattern)


"""

def test_update_async():

def test_dynamics_async():
    hahj



--------------------------- SALOME -------------------------------
"""
def test_storkey_weights():
    #generic values 
    assert np.allclose(f.storkey_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[1.125, 0.25, -0.25, -0.5], [0.25, 0.625, -1, 0.25], [-0.25, -1, 0.625, -0.25], [-0.5, 0.25, -0.25, 1.125]]))
    memorized_patterns = f.generate_patterns(3,4)
    storkey_weight = f.storkey_weights(memorized_patterns)
    assert np.shape(storkey_weight)[0] == 4 #size tests   
    assert np.shape(storkey_weight)[0] == np.shape(storkey_weight)[1]

def test_energy():
    memorized_patterns = f.generate_patterns(3,4)
    energy = f.energy(memorized_patterns)
    update_pattern = []
    for i in range (100): #tests that the energy matrix is non increasing  
        update_pattern = f.update(memorized_patterns, f.hebbian_weights(memorized_patterns))
        i+=1
    assert energy==f.energy(update_pattern) 

def test_flatten_checkerboard():
    checkboard = f.generate_patterns(6,8)
    flatten_checkboard = f.flatten_checkerboard(checkboard)
    assert np.shape(flatten_checkboard)[0] == np.shape(checkboard)[0]* np.shape(checkboard)[1]
    assert np.shape(flatten_checkboard)[1] == 1 

def test_vector_to_matrix():
    pattern = f.generate_patterns(1,2500)
    matrix = f.vector_to_matrix(pattern)
    assert np.shape(pattern)[1] == np.shape(matrix)[0] * np.shape(matrix)[1]
    assert np.shape(matrix)[0]==50
    assert np.shape(matrix)[0] == np.shape(matrix)[1]
    

"""""
-------------------------- MISCHA -------------------------------


def test_generate_initial_checkerboard():
    checkerboard = f.generate_initial_checkerboard()
    f.matrix_element_tests(checkerboard)
    #no easy way to compare a checkerboard with a premaid one 


"""
"""
def test_matrix_list():
    assert np.allclose( f.matrix_list(list((np.ones(2500),-1*np.ones(2500)))) , list((np.ones(np.ones(50)), -1*np.ones(-1*np.ones(50)))) )


def test_pattern_match(): #erreur bizarre n'aimant pas nos types 
    # generic values
    assert f.pattern_match(np.ndarray([1,-1,1],[1,1,1],[-1,-1,1]),[1,1,1]) == [1,1,1]
    assert f.pattern_match(np.ndarray([1,-1,1],[1,1,1],[-1,-1,1]),[1,1,-1]) == None
    # exceptions treated in doctests

------------------------- A QUI VEUT ------------------------------
def test_save_video():
    hahj
    
"""