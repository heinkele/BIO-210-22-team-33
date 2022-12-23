import numpy as np
import functions as f


def experiment(size, num_patterns, weight_rule, num_perturb, num_trials=10, max_iter=100):
    """Function running 1 experiment with the same parameters a total of num_trial times.
    Parameters :
    -----------------
    size : int neuronal network size
    num_patterns : int number of patterns which in the given set
    weight_rule : string "hebbian" or "storkey"
    num_perturb : double percentage of perturbations applied to the initial pattern size 
    num_trials : int by default = 10 , number of times we test the experiment in the given conditions
    max_iter : int maximum number of iterations allowed

    Return : 
    --------------
    results_dict : dictionnary containing 5 keys with match_frac corresponding to the percentage of retrieved patterns for the given experiment, in the given conditions.
    """
    match = 0
    memorized_patterns = f.generate_patterns(num_patterns, size)

    if weight_rule == "hebbian":
        W = f.hebbian_weights(memorized_patterns)
    elif weight_rule == "storkey":
        W = f.storkey_weights(memorized_patterns)

    for i in range(num_trials):  # 10 trials per num pattern
        j = np.random.randint(num_patterns)
        perturbed_pattern = f.perturb_pattern(
            memorized_patterns[j], num_perturb)
        H_dyn = f.dynamics(perturbed_pattern.copy(), W, max_iter)
        if (memorized_patterns[j] == H_dyn[j-1]).all():
            match += 1

    match_frac = match / num_trials
    results_dict = {"network_size": size, "weight_rule": weight_rule, "num_patterns": num_patterns,
                    "num_pertub": num_perturb, "match_frac": match_frac}

    return results_dict


def c(n, rule):
    """Function calculating the capacity of a network for a given n and rule.
    Parameters :
    -----------------
    n : int , number of patterns
    rule : string "hebbian" or "storkey"

    Return : 
    --------------
    value : double corresponding to the capacity
    """
    if rule == 'hebbian':
        return n/(2*np.log10(n))  # log base 10
    elif rule == 'storkey':
        return n/(np.sqrt(2*np.log10(n)))
