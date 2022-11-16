import numpy as np 
import  matplotlib.pyplot as plt 


def generate_patterns(num_patterns, pattern_size):
    """Generate the patterns to memorize
    Parameters :
    -----------------
    num_patterns : int
    pattern_size : int

    Return :
    --------------
    Two dimensional numpy array b
    Each row of b is a random pattern of {1, -1} (num_patterns rows of pattern_size columns)

    Exceptions :
    --------------
    >> generate_patterns(0,2)               #add 1 more > so that it works
    Traceback (most recent call last):
    ...
    ValueError: num_patterns must be > 0
    """
    integer_tests(num_patterns)
    integer_tests(pattern_size)

    my_list =[-1,1]
    b=np.zeros((num_patterns,pattern_size))
    for i in range (num_patterns):
        for j in range (pattern_size):
            b[i][j]+=[np.random.choice(my_list)]
    return b

def perturb_pattern (pattern, num_perturb):

    """Pertube a given pattern
    Parameters :
    -----------------
    pattern : 1 dimensional numpy array (a binary pattern)
    num_perturb : int

    Return :
    --------------
    1 dimensional numpy array p_0 (perturbed pattern)

    Exceptions :
    --------------
    >> perturb_pattern(np.array[1,1,-1],4)
    Traceback (most recent call last):
    ...
    ValueError : pattern.size must be superior to num_perturb
    """
    integer_tests(num_perturb)
    vector_tests(pattern, num_perturb)
    list_element_tests(pattern)

    a = np.random.choice(len(pattern), num_perturb, replace=False)

    p_0 = pattern
    for i in range (num_perturb):
        p_0[a[i]]*=-1

    return p_0 


def pattern_match(memorized_patterns, pattern):

    """Match a pattern with the corresponding memorized one (see if there is a match and where)
    Parameters :
    -----------------
    memorized_paterns : 2 dimensional numpy array (Matrix of the initialized memorized patterns, obtained with generate_patterns)
    pattern : 1 dimensional numpy array (pattern of intersest)

    Return :
    --------------
    None : no match
    l : the index of the row corresponding to the matching pattern. (int)
    """

    for l in range(memorized_patterns.shape[0]):
        if (pattern == memorized_patterns[l]):
            return l

def hebbian_weights(patterns):

    """Apply the hebbian learning rule on some given patterns to create the weight matrix.
    Parameters :
    -----------------
    patterns : 2 dimensional numpy array 

    Return :
    --------------
    W : 2 dimensional numpy array p_0 (weight matrix)
    """

    W=np.zeros((np.shape(patterns)[1],np.shape(patterns)[1]))
    for i in range (np.shape(patterns)[1]):
        for j in range(np.shape(patterns)[1]):
            if i==j : 
                W[i][j]=0
            else :
                for k in range (np.shape(patterns)[0]):
                    W[i][j]+=(1/np.shape(patterns)[0])*patterns[k][i]*patterns[k][j]
    return W

def update2(state, weights):

    """Apply the update rule to a state pattern.
    Parameters :
    -----------------
    state : 1 dimensional numpy array (pattern state)
    weigths : 2 dimensional numpy array (weight matrix)

    Return :
    --------------
    state : 1 dimensional numpy array state (pattern state updtated)
    """

    new_state = np.dot(weights, state)
    print("new_state : ", new_state)
    for k in range (len(new_state)):
        if new_state[k] < 0:
            new_state[k] = -1
        else :
            new_state[k] = 1
    print ("update 2 : ", new_state)
    return new_state


def update_async(state, weights):

    """Apply the asynchronous update rule to a state pattern (only for the i-th component of state)
    Parameters :
    -----------------
    state : 1 dimensional numpy array (pattern state)
    weigths : 2 dimensional numpy array (weight matrix)

    Return :
    --------------
    state : 1 dimensional numpy array state (pattern state with the i-th component updtated)
    """

    i = np.random.randint(0, np.shape(state)[0])
    for j in range (np.shape(weights)[1]):
        if state[i]* weights[i][j] >= 0 :
            state[i] = 1
        else :
            state[i] = -1
    return state

def dynamics(state, weights, max_iter):

    """Run the dynamical system from an initial state until convergence or until a maximum number of steps is reached.
       Convergence is achieved when two consecutive updates return the same state.
    Parameters :
    -----------------
    state : 1 dimensional numpy array (pattern state)
    weigths : 2 dimensional numpy array (weight matrix)
    max_iter : int (maximum of iteration allowed)

    Return :
    --------------
    history : a list with the whole state history. (list of 1 dimensional numpy array)
    """

    T=1 
    u=update2(state, weights)
    history = [u]
    v=update2(u, weights)
    history.append(v) 
    print ("u : ", u)
    print("v : ", v)
    
    while (not(np.array_equal(history[len(history)-1],history[len(history)-2])) and (T < max_iter)) :
        v=update2(v, weights)
        history.append(v)
        T += 1
        print(T)
        print("v : ", v)
    
    return history

def dynamics_async(state, weights, max_iter, convergence_num_iter):

    """Run the dynamical system from an initial state until convergence or until a maximum number of steps is reached.
       Convergence is achieved when the solution does not change for convergence num iter steps in a row
    Parameters :
    -----------------
    state : 1 dimensional numpy array (pattern state)
    weigths : 2 dimensional numpy array (weight matrix)
    max_iter : int (maximum of iteration allowed)
    convergence_num_iter int (criteria of convergence)

    Return :
    --------------
    history : a list with the whole state history. (list of 1 dimensional numpy array)
    """

    T = 1
    u = update_async(state, weights)
    history = [u]
    rep = 0
    while (rep!=convergence_num_iter) and (T < max_iter):
        v=u 
        u = update_async(u, weights)
        if ((v == u).all()):
            rep+=1
        else :
            rep=0
        history.append(u)
    return history

def storkey_weights(patterns):
    """Apply the Storkey learning rule for some patterns to create the weight matrix
    Parameters :
    -----------------
    patterns : 2 dimensional numpy array (some patterns)

    Return :
    --------------
    W : 2 dimensional numpy array (weigth matrix)
    """

    num_patterns = np.shape(patterns)[0]
    pattern_size = np.shape(patterns)[1]
    W = np.zeros((pattern_size,pattern_size))
    W_prev =  W #premier w que de 0
    H=np.zeros((pattern_size, pattern_size))
    for u in range (num_patterns): #nombre de patterns 
        for i in range (pattern_size):
            for j in range (pattern_size):

                for k in range (pattern_size):#code matrix H 
                    if (k!=i and k!=j):
                        H[i][j]+= W_prev[i][k]*patterns[u][k]
    
                W[i][j]=W_prev[i][j]+(patterns[u][i]*patterns[u][j]-patterns[u][i]*H[j][i]-patterns[u][j]*H[i][j])/num_patterns            
        W_prev=W #actualisation de "l'ancienne matrice" 
    print(W)
    return W



def energy(state, weights) :
    """Function that calculates the energy associated to the given pattern
    Parameters :
    -----------------
    state : 2 dimensional numpy array 
    weights : 2 dimensional numpy array (weight matrix)

    Return :
    --------------
    E : float or int
    """
    E=0
    for i in range ():
        for j in range (): 
            E+= weights[i][j]*state[i]* state [j]
    return -1/2*E 

# the update function does not function. do we need to do a deepcopy of state ? we are lost

def generate_initial_checkerboard():
    """Function creating a initial checkerboard with alternate black and white boxes.
    Parameters :
    -----------------
    None
    Return :
    --------------
    checkerboard : 2 D numpy array matrix 
    """
    axis_x = np.ones(50)
    counter = 0
    i=5
    while (i<50) : 
        axis_x[i]*=-1
        counter+=1
        if (counter==5): 
            i+=5
            counter=0
        i+=1
    print ("x:", axis_x)
    axis_y=axis_x.reshape(50,1)
    print ("y:", axis_y)
    checkboard = axis_y*axis_x
    print (checkboard)
    print (checkboard.shape[0], checkboard.shape[1])
    return checkboard

def flatten_checkerboard(checkerboard):
    """Function reshaping a 2D matrix into a 1D array.
    Parameters :
    -----------------
    checkerboard : 2D numpy array matrix
    Return :
    --------------
    flattened_checkerboard : 1D numpy array  
    """
    flattened_checkerboard = checkerboard.reshape(1,2500)
    return flattened_checkerboard 

def vector_to_matrix(pattern):
    """Function reshaping a vector (1D) into a  2D array.
    Parameters :
    -----------------
    pattern : (1D) numpy array 
    Return :
    --------------
    matrix : 2D numpy array  
    """
    matrix = pattern.reshape(50,50) 
    return matrix

def matrix_list(history): 
    """Function adding the given pattern to a list containing multiple patterns.
    Parameters :
    -----------------
    history : (1D) numpy array  
    Return : 
    --------------
    m_list : 2D numpy array (containing multiple patterns)
    """
    m_list = []
    for i in range (history.shape[0]): 
        m_list.append(vector_to_matrix(history[i]))
    return m_list

def save_video(state_list, out_path) : #NB : state_list est la liste renvoyée par la fct précédente  
    """Function generating a video from a sequence of patterns. takes a photo every XX perturbations
    Parameters :
    -----------------
    state_list : 2D numpy array (list of patterns) 
    out_path : video ?????
    Return : 
    --------------
    out_path : video ??????
    """    
    liste=[]
    for i in range (state_list.shape[0]) : #on devra le changer pour iterer seulement toutes les X_X_X modifications
        liste.append(plt.imshow(state_list[i], cmap='gray'))
    out_path=plt.ArtistAnimation(liste)
    return out_path



"""--------------------------------------- ARGUMENT TESTS -------------------------------------------------"""
def integer_tests(arg):
    import math
    if math.floor(arg) != arg:
        raise ValueError(arg, "must be an integer")
    if arg <= 0 :
        raise ValueError(arg, "must > 0")
    if arg+1 == arg :
        raise OverflowError(arg, "too large")

def vector_tests(arg, max_size = None):
    if not isinstance(arg, np.ndarray):
        raise TypeError("Inappropriate type :", arg, "must be a np.ndarray")
    if (arg.size < max_size):
        raise ValueError(arg, "must be superior to", max_size)

def list_element_tests(pattern, possible_values = [1, -1]):
    if (not all(m in pattern for m in possible_values)):
        raise ValueError(pattern, "should only contain values in", possible_values)