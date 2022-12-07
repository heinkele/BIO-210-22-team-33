import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

class Patterns:
    def __init__(self, num_patterns, pattern_size, patterns=0):
        self.num_patterns = num_patterns
        self.pattern_size = pattern_size
        self.patterns = patterns

    def generate_patterns(self):
        self.patterns = np.random.choice(np.array([-1, 1]), size=(self.num_patterns, self.pattern_size))

    def perturb_patterns(self, pattern, num_perturb):
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

        pattern = pattern.copy()  # deep copy to iterate on the pattern and modify it
        for i in range(num_perturb):
            pattern[a[i]] *= -1

        return pattern


    def pattern_match(self):
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
        for l in range(np.shape(self.patterns)[0]):
            if (self.pattern == self.patterns[l]).all():
                return l

    def generate_initial_checkerboard(self):
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
        i = 5  # we iterate every 5 values to create 5x5 checkers
        while (i < 50):
            axis_x[i] *= -1
            counter += 1
            if (counter == 5):  # we iterate every 5 values to create 5x5 checkers
                i += 5
                counter = 0
            i += 1
        # we use the diagnal symetry of the checkboard
        axis_y = axis_x.reshape(50, 1)
        checkboard = axis_y*axis_x
        return checkboard

class HopfieldNetwork:
    def __init__(self, patterns, rule="hebbian"):
        if rule == "hebbian" :
            self.weights = HopfieldNetwork.hebbian_weigths(patterns)
        if rule == "storkey":
            self.weights = HopfieldNetwork.storkey_weights(patterns)
            


    def hebbian_weights(self, patterns):
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
        W = np.zeros((np.shape(patterns)[1], np.shape(patterns)[1]))
        for u in range(np.shape(patterns)[0]):
            W += (1/np.shape(patterns)[0])*np.outer(patterns[u], patterns[u])
            np.fill_diagonal(W, 0)
        return W

    def storkey_weights(self, patterns):

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

    def update(self, state):
        """Apply the update rule to a state pattern.
        Parameters :
        -----------------
        state : 1 dimensional numpy array (pattern state)
        weigths : 2 dimensional numpy array (weight matrix)

        Return :
        --------------
        state : 1 dimensional numpy array state (pattern state updtated)
        """
        new_state = np.dot(self.weights, state)
        return np.where(new_state >= 0, 1, -1)

    def update_async(self, state):
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
        value = np.dot(state, self.weights[i])
        new_state = state.copy()
        if value >= 0:
            new_state[i] = 1
        else:
            new_state[i] = -1
        return new_state
    
    def dynamics(self, state, saver, max_iter=20):
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
        t = 0  # counter that increases if the pattern doesn't change (to see if we reach convergence_num_iter)
        old_state = np.zeros(len(state))
        saver.data["state"].append(state)
        saver.date["energy"].append(self.compute_energy(state))

        while (state != old_state).any() and (t < max_iter):
            old_state = state
            state = self.update(state, self.weights)
            saver.data["state"].append(state)
            saver.date["energy"].append(self.compute_energy(state))            
            t += 1
        return saver
    
    def dynamics_async(self, state, saver, max_iter=1000, convergence_num_iter=100, skip=10):
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
        # counter that increases if the pattern doesn't change (to see if we reach convergence_num_iter)
        rep = 0
        saver.data["state"].append(state)
        saver.data["energy"].append(self.compute_energy(state))
        while (rep != convergence_num_iter) and (t < max_iter):
            old_state = state
            state = self.update_async(state, self.weights)
            if (state == old_state).all():
                rep += 1
            else:
                rep = 0
            if t % skip == 0:
                saver.data["state"].append(state)
                saver.date["energy"].append(self.compute_energy(state))
            t += 1
        return saver
    
class DataSaver:

    def __init__(self):
        self.data = {"state": [], "energy": []}

    def reset(self):
        self.data = {
            "pattern" : [],
            "rule" : []
        }

    def store_iter(self, state, weights):
        if state is not None:
            self.data["state"].append(state.copy())
        if state is not None:
            self.data["energy"].append(self.compute_energy(state, weights))


    def compute_energy(self, state, weights):
        """Function that calculates the energy associated to the given pattern
        Parameters :
        -----------------
        state : 2 dimensional numpy array 
        weights : 2 dimensional numpy array (weight matrix)

        Return :
        --------------
        e : float or int : energy of the network 
        """

        return -(1/2)*np.sum(weights * np.outer(state, state))
    
    def get_data(self):
        return self.data

    def save_video(self, out_path, img_shape):
        """
        Function generating a video from a sequence of patterns.
        Parameters :
        -----------------
        state_list : 2D numpy array (list of patterns) 
        out_path : path saving the video, needs to be an argument to be accessible as long as we need the function 
        Return : 
        --------------
        out_path : path saving the video 
        """
        fig = plt.figure()
        liste = []
        for i in self.saver.data["state"]:
            liste.append([plt.imshow(i.reshape(50, 50), cmap='gray')])
        my_anim = anim.ArtistAnimation(fig, liste)
        my_anim.save(out_path)
    
    def plot_energy(self):
        plt.figure
        plt.title(self.rule)
        plt.plot(self.get_data())
        plt.show()

