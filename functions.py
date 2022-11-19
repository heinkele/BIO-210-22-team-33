import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as anim


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
    my_list =[-1,1]
    b=np.zeros((num_patterns,pattern_size))
    for i in range(num_patterns):
        for j in range(pattern_size):
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
    a = np.random.choice(len(pattern), num_perturb, replace=False)
    
    p_0 = pattern.copy()
    for i in range (num_perturb):
        p_0[a[i]]*=-1

    return p_0 

def pattern_match(memorized_patterns, pattern): #problème : considère memorized patterns comme une liste au lie dun ndarray
    """
    Match a pattern with the corresponding memorized one (see if there is a match and where)
    Parameters :
    -----------------
    memorized_patterns : 2 dimensional numpy array (Matrix of the initialized memorized patterns, obtained with generate_patterns)
    pattern : 1 dimensional numpy array (pattern of intersest)

    Return :
    --------------
    None : no match
    l : the index of the row corresponding to the matching pattern. (int)

    Exceptions :
    --------------
    >>pattern_match([[1,-1],[1,2]])
    Traceback (most recent call last):
    ...
    ValueError : pattern should only contain values in [-1,1]
    """
    for l in range(memorized_patterns.shape[0]):
        if ((pattern == memorized_patterns[l]).all()):
            return l

def hebbian_weights(patterns):
    """Apply the hebbian learning rule on some given patterns to create the weight matrix.
    Parameters :
    -----------------
    patterns : 2 dimensional numpy array 

    Return :
    --------------
    W : 2 dimensional numpy array p_0 (weight matrix)

    Exceptions :
    --------------
    >> hebbian_weights(np.array([[1,1,-1], [2, 1, -1]]))
    Traceback (most recent call last):
    ...
    ValueError : elements of patterns must be 1 or -1
    """
    W=np.zeros((np.shape(patterns)[1],np.shape(patterns)[1]))
    for u in range (np.shape(patterns)[0]):
        W += (1/np.shape(patterns)[0])*np.outer(patterns[u], patterns[u])
        np.fill_diagonal(W, 0)
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
    new_state = np.dot(weights, state)
    for k in range (len(new_state)):
        if new_state[k] < 0:
            new_state[k] = -1
        else :
            new_state[k] = 1
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
    i = np.random.randint(len(state))
    value = np.dot(state, weights[i])
    new_state = state.copy()
    #np.where(state[i])
    if value >= 0 :
        new_state[i] = 1
    else :
        new_state[i] = -1
    return new_state

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
    t=0
    old_state = np.zeros(len(state))
    history = [state] 
    
    while (state != old_state).any() and t < max_iter :
        old_state = state
        state=update(state, weights)
        history.append(state)
        t += 1

    print("history : ", history)
    print(t)
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

    t = 0
    rep = 0 #counter that increases if the pattern doesn't change (to see if we reach convergence_num_iter)
    history = [state]
    while (rep!=convergence_num_iter) and (t < max_iter):
        old_state=state
        state = update_async(state, weights)
        if (state == old_state).all():
            rep+=1
        else :
            rep=0
        if t%1000 == 0:
            history.append(state)
        t+=1
    print(t)
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

    """"
    for u in range (num_patterns): #nombre de patterns 
        for i in range (pattern_size):  
            for j in range (pattern_size):

                for k in range (pattern_size):#code matrix H 
                    if (k!=i and k!=j):
                        H[i][j]+= W_prev[i][k]*patterns[u][k]
    
                W[i][j]=W_prev[i][j]+(patterns[u][i]*patterns[u][j]-patterns[u][i]*H[j][i]-patterns[u][j]*H[i][j])/num_patterns   

        for i in range (pattern_size):#code matrix H
            H += np.dot(W_prev[i], patterns[u])

        W = W_prev + (np.outer(patterns[u], patterns[u]) - np.outer(patterns[u], H[u]) - np.outer(patterns[u], H[u]))/ num_patterns    

        W_prev=W #actualisation de "l'ancienne matrice" 
    """

    num_patterns = np.shape(patterns)[0]
    pattern_size = np.shape(patterns)[1]
    W = np.zeros((pattern_size,pattern_size))
    W_prev =  W #premier w que de 0
    H=np.zeros((pattern_size, pattern_size))

    for u in range (num_patterns) :
        H += W_prev@patterns[u]
        np.reshape(H, (1, pattern_size*pattern_size))
        case_i_eq_k = np.diag(W_prev)*patterns[u]
        W_prev_diag_eq_0 = W_prev
        np.fill_diagonal(W_prev_diag_eq_0, 0)
        case_j_eq_k = W_prev_diag_eq_0*patterns[u]
        H -= case_i_eq_k + case_j_eq_k
        np.reshape(H, (pattern_size, pattern_size))
        W = W_prev + (1/num_patterns)*(np.outer(patterns[u], patterns[u]) - patterns[u] * H - np.transpose(patterns[u]*H))
        W_prev = W
    return W
  
def energy(state, weights) :
    """Function that calculates the energy associated to the given pattern
    Parameters :
    -----------------
    state : 2 dimensional numpy array 
    weights : 2 dimensional numpy array (weight matrix)

    Return :
    --------------
    e : float or int : energy of the network 
    """
    return -(1/2)*np.sum(weights * np.outer(state,state))

def generate_initial_checkerboard(): 
    """Function creating a initial checkerboard with alternate black and white boxes : A 50x50 checkerboard with 5x5 checkers
    Parameters :
    -----------------
    None
    Return :
    --------------
    checkerboard : 2 D numpy array matrix 
    """
    axis_x = np.ones(50)
    counter = 0
    i=5 # we iterate every 5 values to create 5x5 checkers 
    while (i<50) : 
        axis_x[i]*=-1
        counter+=1
        if (counter==5): # we iterate every 5 values to create 5x5 checkers 
            i+=5
            counter=0
        i+=1
    axis_y=axis_x.reshape(50,1) #we use the diagnal symetry of the checkboard 
    checkboard = axis_y*axis_x 
    return checkboard

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

def save_video(state_list, out_path) :   
    """Function generating a video from a sequence of patterns. takes a photo every XX perturbations
    Parameters :
    -----------------
    state_list : 2D numpy array (list of patterns) 
    out_path : path saving the video, needs to be an argument to be accessible as long as we need the function 
    Return : 
    --------------
    out_path : path saving the video 
    """    
    fig = plt.figure()
    liste=[]
    for i in state_list : 
        liste.append([plt.imshow(i.reshape(50,50), cmap='gray')]) 
    my_anim=anim.ArtistAnimation(fig,liste)
    my_anim.save(out_path)


def plot_energy(history, weights,  step=1) : 
    energydict = {}
    i=0
    while i < np.shape(history)[0] :
        energydict[i]=energy(history[i],weights)
        i += step
    return energydict