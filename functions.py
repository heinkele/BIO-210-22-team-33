from sre_parse import State
import numpy as np 

def generate_patterns(num_patterns, pattern_size):
    my_list =[-1,1]
    a=[np.random.choice(my_list,pattern_size) for j in range(num_patterns)]
    return a

def generate_coord(num_patterns,pattern_size):
    x=np.random.randint(num_patterns)
    y=np.random.randint(pattern_size)
    return [x,y]

def perturb_pattern(pattern, num_perturb):
    list_coord=[]
    for i in range (num_perturb):
       # new_coord=generate_coord(pattern.shape[0],pattern.shape[1])
        condition=False
        if i>2:
            for k in range (i-1):
                if [list_coord(k),list_coord(k+1)]!=generate_coord(pattern.shape[0],pattern.shape[1]):
                    condition=True
                else :
                    condition=False
                    break
        if condition==True:
            list_coord.append(generate_coord(pattern.shape[0],pattern.shape[1]))
    
    p_0 = pattern
    for i in range (num_perturb):
        p_0[list_coord[i]]*=-1

    return p_0 

def pattern_match(memorized_patterns, pattern):
    for l in range(memorized_patterns.shape[0]):
        if (pattern == memorized_patterns[l]):
            return l

def hebbian_weights(patterns):
    W=np.zeros((50,50))
    for i in range (patterns.shape[1]):
        for j in range(patterns.shape[1]):
            if i==j : 
                W[i][j]=0
            else :
                for k in range (patterns.shape[0]):
                    W[i][j]+=(1/patterns.shape[0])*patterns[k][i]*patterns[k][j]
    return W

def update(state, weights): 
    for i in range (state.shape[0]) : 
        for j in range (state.shape[1]) : 
            if state[i][j] * weights[i][j] >= 0 :
                state[i][j] = 1
            else :
                state[i][j] = -1
    return state

def update_async(state, weights):
    i = np.random.randint(0, state.shape[0])
    for j in range (state.shape[1]):
        if state[i][j] * weights[i][j] >= 0 :
            state[i][j] = 1
        else :
            state[i][j] = -1
    return state

def dynamics(state, weights, max_iter):
    T=1
    u=update(state, weights)
    history = [u]
    while (state != u) and (T < max_iter) : 
        u=update(u, weights)
        history.append(u)
        T += 1
    return history

def dynamics_async(state, weights, max_iter, convergence_num_iter):
    T = 1
    u = update_async(state, weights)
    history = [u]
    rep = 0
    while (rep!=convergence_num_iter) and (T < max_iter):
        v=u 
        u = update_async(u, weights)
        if (v == u):
            rep+=1
        else :
            rep=0
        history.append(u)
    return history
    