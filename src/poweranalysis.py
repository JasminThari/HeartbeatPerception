#%%
import numpy as np
from statsmodels.stats.power import FTestAnovaPower

# Initialize the power analysis object
analysis = FTestAnovaPower()

# Define parameters
effect_size = 0.8  # Medium effect size (Cohen's f)
alpha = 0.05        # Significance level
power = 0.95       # Desired power
k_groups = 3       # Number of groups

# Calculate the required sample size per group
sample_size = analysis.solve_power(effect_size=effect_size, 
                                   alpha=alpha, 
                                   power=power, 
                                   k_groups=k_groups)

print(f"Required sample size per group: {np.ceil(sample_size)}")
#%%