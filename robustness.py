import numpy as np
import functions as f

def robustness (sizes, weight_rule, percentage, num_trials=10, max_iter=100, num_patterns = 2):
    
    match = 0

    for s in range (len(sizes)):

        memorized_patterns = f.generate_patterns(num_patterns, sizes[s])
        num_perturb = int(percentage*sizes[s])

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

    return match / (len(sizes) * num_trials)
 