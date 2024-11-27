#%%
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the data
df = pd.read_csv('../Data/Results/results.csv')

# Calculate correctness
df['Correct'] = df.apply(lambda row: 1 if row['Response'] == row['Actuals'] else 0, axis=1)

# Calculate proportion correct per participant
df['Proportion'] = df.groupby(['Participant_ID'])['Correct'].transform('mean')

# Prepare the dataframe for statistical analysis
df_proportions = df.drop_duplicates(subset=['Participant_ID'])[['Participant_ID', 'Experiment_Num', 'Proportion', 'Gender']]

# Ensure 'Experiment_Num' is treated as a categorical variable
df_proportions['Experiment_Num'] = df_proportions['Experiment_Num'].astype('category')

#%% Visualize the distribution of proportions

# Boxplot to visualize the distribution of proportions across experiments
plt.figure(figsize=(10, 6))
sns.boxplot(x='Experiment_Num', y='Proportion', data=df_proportions)
plt.title('Distribution of Proportion Correct Across Experiments')
plt.xlabel('Experiment Number')
plt.ylabel('Proportion Correct')
plt.show()

# Violin plot for a more detailed distribution
plt.figure(figsize=(10, 6))
sns.violinplot(x='Experiment_Num', y='Proportion', data=df_proportions, inner='quartile')
plt.title('Violin Plot of Proportion Correct Across Experiments')
plt.xlabel('Experiment Number')
plt.ylabel('Proportion Correct')
plt.show()

# Summary statistics
print(df_proportions.groupby('Experiment_Num')['Proportion'].describe())

#%% Perform one-sample t-test
for experiment in df_proportions['Experiment_Num'].unique():
    print(f"Experiment {experiment}")
    proportions = df_proportions.query("Experiment_Num==@experiment")['Proportion']
    
    # Perform one-sample t-test against chance level (0.5)
    t_statistic, p_value = stats.ttest_1samp(proportions, 0.5)
    
    print("T-statistic:", t_statistic)
    print("P-value:", p_value)
    
    if p_value < 0.05:
        print("Participants performed significantly better than chance.")
    else:
        print("No significant difference from chance performance.")

    # Calculate Cohen's d
    mean_difference = abs(np.mean(proportions) - 0.5)
    std_dev = np.std(proportions, ddof=1)
    cohen_d = mean_difference / std_dev

    print("Cohen's d:", cohen_d)
    print()
#%% # Perform One-Way ANOVA
groups = [group["Proportion"].values for name, group in df_proportions.groupby("Experiment_Num")]

# Perform the ANOVA
f_stat, p_val = stats.f_oneway(*groups)

print("One-Way ANOVA results:")
print(f"F-statistic: {f_stat}")
print(f"P-value: {p_val}")

if p_val < 0.05:
    print("Reject the null hypothesis: There is a significant difference between the experiments.")
else:
    print("Fail to reject the null hypothesis: No significant difference between the experiments.")


# %% Perform One-Way ANOVA using Statsmodels
model = ols('Proportion ~ C(Experiment_Num)', data=df_proportions).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("ANOVA Table:")
print(anova_table)

#%% Q-Q plot for residuals
sns.set(style="whitegrid", palette="muted", color_codes=True)
# 1. Q-Q Plot for Residuals
fig, ax = plt.subplots(figsize=(8, 6))
sm.qqplot(model.resid, line='s', ax=ax, markersize=5)
ax.set_title('Q-Q Plot of ANOVA Residuals')
sns.despine()
plt.show()
# 2. Residuals Distribution Plot
plt.figure(figsize=(8, 6))
sns.histplot(model.resid, kde=True, bins=20, color='skyblue')
plt.title('Distribution of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
sns.despine()
plt.show()


#%% Shapiro-Wilk test for each group
for name, group in df_proportions.groupby('Experiment_Num'):
    stat, p = stats.shapiro(group['Proportion'])
    print(f'Experiment {name} - Shapiro-Wilk test: Statistics={stat:.3f}, p={p:.3f}')
    if p > 0.05:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')


# %% Levene’s Test
levene_stat, levene_p = stats.levene(*groups)
print(f"Levene’s Test: Statistics={levene_stat:.3f}, p={levene_p:.3f}")

if levene_p > 0.05:
    print("Variances are equal (fail to reject H0)")
else:
    print("Variances are not equal (reject H0)")


