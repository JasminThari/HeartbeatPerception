


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
grouped_df = df.groupby(['Experiment_Num', 'trial_num'])['Correct'].mean().reset_index()

# Rename 'Correct' to 'Proportion_Correct' for clarity
grouped_df.rename(columns={'Correct': 'Proportion_Correct'}, inplace=True)

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Initialize the matplotlib figure
plt.figure(figsize=(15, 6))

# Create the line plot
sns.lineplot(
    data=grouped_df,
    x='trial_num',
    y='Proportion_Correct',
    hue='Experiment_Num',
    style='Experiment_Num',  # This ensures different line styles
    markers=True,            # Optional: Adds markers to the lines
    dashes=True,             # Use default dash patterns for different styles
    linewidth=2, 
    palette='ch:s=.25,rot=-.25'
)

# Customize the plot
plt.title('Proportion of Correct Responses Across Trials by Group', fontsize=16)
plt.xlabel('Trial Number', fontsize=14)
plt.ylabel('Proportion Correct', fontsize=14)
plt.legend(title='Group', fontsize=12, title_fontsize=13)
plt.xticks(grouped_df['trial_num'].unique())  # Ensure all trial numbers are shown

# Show the plot
plt.tight_layout()
plt.show()

# %%
grouped_df = df.groupby(['Pair_ID', 'Experiment_Num'])['Correct'].mean().reset_index()

# Rename 'Correct' to 'Proportion_Correct' for clarity
grouped_df.rename(columns={'Correct': 'Proportion_Correct'}, inplace=True)

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Initialize the matplotlib figure
plt.figure(figsize=(25, 6))

# Create the line plot
sns.lineplot(
    data=grouped_df,
    x='Pair_ID',
    y='Proportion_Correct',
    hue='Experiment_Num',
    style='Experiment_Num',  # This ensures different line styles
    markers=True,            # Optional: Adds markers to the lines
    dashes=True,             # Use default dash patterns for different styles
    linewidth=2
)

# Customize the plot
plt.title('Proportion of Correct Responses Across Trials by Group', fontsize=16)
plt.xlabel('Trial Number', fontsize=14)
plt.ylabel('Proportion Correct', fontsize=14)
plt.legend(title='Group', fontsize=12, title_fontsize=13)
plt.xticks(grouped_df['Pair_ID'].unique())  # Ensure all trial numbers are shown

# Show the plot
plt.tight_layout()
plt.show()
# %%
