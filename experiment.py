import numpy as np
import functions as f
from math import log, sqrt

def experiment(size, num_patterns, weight_rule, num_perturb, num_trials=10, max_iter=100):

    match = 0
    memorized_patterns = f.generate_patterns(num_patterns, size)

    for i in range (num_trials):
        j = np.random.randint(num_patterns)
        perturbed_pattern = f.perturb_pattern(memorized_patterns[j], num_perturb)
        if weight_rule == "hebbian":
            W = f.hebbian_weights(memorized_patterns)
            H_dyn = f.dynamics(perturbed_pattern.copy(), W, max_iter)
            if (memorized_patterns[j] == H_dyn[-1]).all():
                match += 1
                
        elif weight_rule == "storkey":
            W = f.storkey_weights(memorized_patterns)
            H_dyn = f.dynamics(perturbed_pattern.copy(), W, max_iter)
            if (memorized_patterns[j] == H_dyn[-1]).all():
                match += 1
    
    match_frac = match / num_trials
    results_dict = {"network_size" : size, "weight_rule": weight_rule, "num_patterns" : num_patterns,
                    "num_pertub" : num_perturb, "match_frac" : match_frac}

    return results_dict

def c(n, rule):
    if rule == 'hebbian' :
        return n/(2*np.log10(n))  #log base 10
    elif rule == 'storkey' :
        return n/(np.sqrt(2*np.log10(n)))