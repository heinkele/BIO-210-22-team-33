import numpy as np

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
    W = np.zeros((pattern_size, pattern_size))
    W_prev = W.copy()  # premier w que de 0

    for u in range(num_patterns):
        #H = W_prev@patterns[u]
        H = np.reshape((W_prev@patterns[u]), (pattern_size, 1))
        case_i_eq_k = np.diag(W_prev)*patterns[u]
        case_i_eq_k = np.reshape(case_i_eq_k, (pattern_size, 1))
        W_prev_diag_eq_0 = W_prev.copy()
        np.fill_diagonal(W_prev_diag_eq_0, 0)
        case_j_eq_k = W_prev_diag_eq_0*patterns[u]
        H = H - case_i_eq_k - case_j_eq_k
        np.reshape(H, (pattern_size, pattern_size))
        W = W_prev + (1/pattern_size)*(np.outer(
            patterns[u], patterns[u]) - patterns[u] * H - np.transpose(patterns[u]*H))
        W_prev = W
    return W