#%%
import numpy as np
from statsmodels.stats.power import FTestAnovaPower

# Initialize the power analysis object
analysis = FTestAnovaPower()

# Define parameters
effect_size = 0.8  # Medium effect size (Cohen's f)
alpha = 0.05        # Significance level
power = 0.80        # Desired power
k_groups = 3        # Number of groups

# Calculate the required sample size per group
sample_size = analysis.solve_power(effect_size=effect_size, 
                                   alpha=alpha, 
                                   power=power, 
                                   k_groups=k_groups)

print(f"Required sample size per group: {np.ceil(sample_size)}")
#%%

import pingouin as pg

# Perform power analysis for ANOVA
power = pg.power_anova(eta_squared=0.175, 
                       k=3, 
                       alpha=0.05, 
                       power=0.80, 
                       n=None)

print(f"Required sample size per group: {np.ceil(power)}")
# %%
