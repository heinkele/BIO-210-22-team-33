import functions as f
import numpy as np


def test_generate_patterns ():
    M = f.generate_patterns(3,4)
    assert M.shape[0] == 3  #size tests
    assert M.shape[1] == 4
    assert all(m in M for m in [1, -1]) #value tests

def test_perturb_pattern():
    t = list(f.perturb_pattern(np.ones(50),20))
    assert t.count(-1) == 20
    assert all(m in t for m in [1, -1]) #value tests

""""
--------------------------- HUGO -------------------------------

"""

def test_hebbian_weights():
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

def test_update_async():
    memorized_patterns = f.generate_patterns(2, 10)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[1], 5)
    W_h= f.hebbian_weights(memorized_patterns)
    #do same for stokey when it works
    updated_pattern = f.update_async(perturbed_pattern, W_h)
    compar = list(perturbed_pattern - updated_pattern)
    assert (compar.count(0) == (len(updated_pattern)-1) and (compar.count(2) == 1 or compar.count(-2) == 1)) or (compar.count(0) == len(updated_pattern)) #only one element has changed or nothing changed



def test_dynamics(): #soucis de conceptualisation
    memorized_patterns = f.generate_patterns(8, 1000)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[2], 200)
    W= f.hebbian_weights(memorized_patterns)
    #do same with stockey when it works
    history = f.dynamics(perturbed_pattern, W, 20) 

    assert np.shape(history)[0] <= 20  #max iteration
    if np.shape(history)[0] < 20 :
        assert (history[-1] == history[-2]).all() #convergence

def test_dynamic_async():
    memorized_patterns = f.generate_patterns(8, 1000)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[2], 200)
    W= f.hebbian_weights(memorized_patterns)
    #do same with stockey when it works
    history = f.dynamics_async(perturbed_pattern, W, 20000, 3000) 

    assert np.shape(history)[0] <= 20 #max iteration 1/1000 elements in history
    if np.shape(history)[0] < 20 :
        assert (history[-1] == history[-2]).all and (history[-2] == history[-3]).all() #convergence

    #coder cas inverse peut-etre..., voir si augmentation coverage plus tard


"""--------------------------- SALOME ------------------------------- """

def test_storkey_weights():
    #generic values 
    assert np.allclose(f.storkey_weights([[1, 1, -1, -1], [1, 1, -1, 1], [-1, 1, -1, 1]]), ([[1.125, 0.25, -0.25, -0.5], [0.25, 0.625, -1, 0.25], [-0.25, -1, 0.625, -0.25], [-0.5, 0.25, -0.25, 1.125]]))
    memorized_patterns = f.generate_patterns(3,4)
    storkey_weight = f.storkey_weights(memorized_patterns)
    assert np.shape(storkey_weight)[0] == 4 #size tests   
    assert np.shape(storkey_weight)[0] == np.shape(storkey_weight)[1]

#je sais pas si on peut tester juste un return d'une valeur... A part verifier qu'elle est bien négative à la limite, je pense pas qu'il faille faire de tests pour cette fonction
def test_energy():
    memorized_patterns = np.array([1, -1])
    W = np.array([[0, 1/3], [1/3, 0]])
    assert f.energy(memorized_patterns, W) == 1/3


"""
-------------------------- MISCHA -------------------------------
"""


def test_generate_initial_checkerboard():
    checkerboard = (np.reshape(f.generate_initial_checkerboard(), (-1))).tolist()
    assert checkerboard.count(1.) == 1250
    assert checkerboard.count(-1.) == 1250


def test_pattern_match(): #erreur bizarre n'aimant pas nos types 
    assert f.pattern_match(np.array([[1,-1,1],[1,1,1],[-1,-1,1]]),np.array([1,1,1])) == 1
    assert f.pattern_match(np.array([[1,-1,1],[1,1,1],[-1,-1,1]]),[1,1,-1]) == None
"""
------------------------- A QUI VEUT ------------------------------
def test_save_video():
    hahj
    
"""

def test_plot_energy():
    memorized_patterns = f.generate_patterns(8, 1000)
    perturbed_pattern = f.perturb_pattern(memorized_patterns[2], 200)
    W= f.hebbian_weights(memorized_patterns)
    #same with stokey
    history = f.dynamics(perturbed_pattern, W, 20) 
    dict = list(f.plot_energy(history, W).values())
    for i in range (len(dict)-1) :
        assert dict[i] >= dict[i+1] #non-increasing

