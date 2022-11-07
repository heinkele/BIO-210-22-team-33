from sre_parse import State
import numpy as np 

def generate_patterns(num_patterns, pattern_size):
    my_list =[-1,1]
    b=np.zeros((num_patterns,pattern_size))
    for i in range (num_patterns):
        for j in range (pattern_size):
            b[i][j]+=[np.random.choice(my_list)]
    return b

def generate_coord(pattern_size):
    x=np.random.randint(pattern_size)
    return x

def perturb_pattern(pattern, num_perturb):
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
    for l in range(memorized_patterns.shape[0]):
        if (pattern == memorized_patterns[l]):
            return l

def hebbian_weights(patterns):
    W=np.zeros((patterns.shape[1],patterns.shape[1]))
    for i in range (patterns.shape[0]):
        for j in range(patterns.shape[1]):
            if i==j : 
                W[i][j]=0
            else :
                for k in range (patterns.shape[0]):
                    W[i][j]+=(1/patterns.shape[0])*patterns[k][i]*patterns[k][j]
    return W

def update(state, weights):
    for i in range (state.shape[0]) : 
        for j in range (weights.shape[1]) : 
            if state[i] * weights[i][j] >= 0 :
                state[i] = 1
            else :
                state[i] = -1
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
    while (state.all() != u.all()) and (T < max_iter) : 
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

def storkey_weights(patterns):
    num_patterns = patterns.shape[0]
    pattern_size = patterns.shape[1]
    W = np.zeros((pattern_size,num_patterns))
    W_prev =  W #premier w que de 0
    H=np.array((num_patterns, num_patterns))
    for u in range (num_patterns): #numero du pattern 
        for i in range (1,num_patterns):
            for j in range (num_patterns):

                for k in range (patterns.shape[1]):#code matrix H 
                    if (k!=i and k!=j):
                        H[i][j]+= W_prev[i][k]*patterns[u][k]
    
                W[i][j]=W_prev[i][j]+(patterns[u][i]*patterns[u][j]-patterns[u][i]*H[j][i]-patterns[u][j]*H[i][j])/num_patterns            
        W_prev=W #actualisation de "l'ancienne matrice" 
    return W