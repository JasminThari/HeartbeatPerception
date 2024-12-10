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

#%% Group by trail_num and calculate the mean proportion correct

# Group by 'Experiment_Num' and 'trial_num' and calculate mean of 'Correct'
grouped_trial = df.groupby(['trial_num'])['Correct'].mean().reset_index()
grouped_df = df.groupby(['Experiment_Num', 'trial_num'])['Correct'].mean().reset_index()
grouped_trial['Experiment_Num'] = 'All'
grouped_df = pd.concat([grouped_df, grouped_trial], ignore_index=True)

# Rename 'Correct' to 'Proportion_Correct' for clarity
grouped_df.rename(columns={'Correct': 'Proportion_Correct'}, inplace=True)

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Initialize the matplotlib figure
plt.figure(figsize=(19, 7))

# Create the line plot with customized styles
sns.lineplot(
    data=grouped_df,
    x='trial_num',
    y='Proportion_Correct',
    hue='Experiment_Num',
    style='Experiment_Num',
    palette={exp: 'black' if exp == 'All' else f'C{i}' for i, exp in enumerate(grouped_df['Experiment_Num'].unique())},
    dashes={exp: '' if exp == 'All' else (2, 2) for exp in grouped_df['Experiment_Num'].unique()},
    linewidth=2
)

# Customize the plot
plt.title('Proportion of Correct Responses Across Trials by Group', fontsize=23)
plt.xlabel('Trial Number', fontsize=21)
plt.ylabel('Proportion Correct', fontsize=21)
plt.legend(title='Group', fontsize=16, title_fontsize=16)
plt.xticks(grouped_df['trial_num'].unique(), fontsize=20, rotation=90)  # Adjust the fontsize and rotation as needed
plt.yticks(fontsize=20)  # Adjust the fontsize as needed
# Show the plot
plt.tight_layout()
plt.show()



# %%
