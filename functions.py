from sre_parse import State
import numpy as np 

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
    """

    my_list =[-1,1]
    b=np.zeros((num_patterns,pattern_size))
    for i in range (num_patterns):
        for j in range (pattern_size):
            b[i][j]+=[np.random.choice(my_list)]
    return b

def generate_coord(pattern_size):

    """Generate a random number which represent the coordonnate of the element we want to reach in the pattern"""

    x=np.random.randint(pattern_size)
    return x

def perturb_pattern(pattern, num_perturb):

    """Pertube a given pattern
    Parameters :
    -----------------
    pattern : 1 dimensional numpy array (a binary pattern)
    num_perturb : int

    Return :
    --------------
    1 dimensional numpy array p_0 (perturbed pattern)
    """

    list_coord=[generate_coord(pattern.shape)]
    for i in range (1,num_perturb):
        counter = 0
        new_coord=generate_coord(pattern.shape)
        for k in range (i-1):
            if list_coord[k]!=new_coord :
                counter+=1
                if counter==i-1 :
                    break 
            else :
                new_coord=generate_coord(pattern.shape)
                k=-1 #on recommence le test d'egalite de 0 (k sera incremente au debut de la boucle for et vaudra donc 0)
                counter=0
            k+=1
        list_coord.append(new_coord)
        i+=1
    
    p_0 = pattern
    for i in range (num_perturb):
        p_0[list_coord[i]]*=-1

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

    W=np.zeros((patterns.shape[1],patterns.shape[1]))
    for i in range (patterns.shape[1]):
        for j in range(patterns.shape[1]):
            if i==j : 
                W[i][j]=0
            else :
                for k in range (patterns.shape[0]):
                    W[i][j]+=(1/patterns.shape[0])*patterns[k][i]*patterns[k][j]
    return W

def update(state, weights):

    """Apply the update rule to a state pattern.
    Parameters :
    -----------------
    state : 1 dimensional numpy array (pattern state)
    weigths : 2 dimensional numpy array (weight matrix)

    Return :
    --------------
    state : 1 dimensional numpy array state (pattern state updtated)
    """
    for i in range (state.shape[0]) : 
        for j in range (weights.shape[1]) : 
            if state[i] * weights[i][j] >= 0 :
                state[i] = 1
            else :
                state[i] = -1
    return state

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

    i = np.random.randint(0, state.shape[0])
    for j in range (weights.shape[1]):
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
    s=state.copy() 
    u=update(state, weights)
    u=update(u, weights)
    history = [u]
    
    while ((s!= u).any()) and (T < max_iter) :
        u=update(u, weights)
        history.append(u)
        T += 1
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

    num_patterns = patterns.shape[0]
    pattern_size = patterns.shape[1]
    W = np.zeros((pattern_size,num_patterns))
    W_prev =  W #premier w que de 0
    H=np.array((num_patterns, num_patterns))
    for u in range (num_patterns): #nombre de patterns 
        for i in range (1,num_patterns):
            for j in range (num_patterns):

                for k in range (patterns.shape[1]):#code matrix H 
                    if (k!=i and k!=j):
                        H[i][j]+= W_prev[i][k]*patterns[u][k]
    
                W[i][j]=W_prev[i][j]+(patterns[u][i]*patterns[u][j]-patterns[u][i]*H[j][i]-patterns[u][j]*H[i][j])/num_patterns            
        W_prev=W #actualisation de "l'ancienne matrice" 
    return W



def energy(state, weights) :
    """Function that calculates the energy 
    """
    E=0
    for i in range ():
        for j in range (): 
            E+= weights[i][j]*state[i]* state [j]
    return -1/2*E 

# the update function does not function. do we need to do a deepcopy of state ? we are lost

def generate_checkerboard():
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