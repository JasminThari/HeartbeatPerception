import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(100)
df = pd.read_csv('../Data/Results/results.csv')

# Correctness
df['Correct'] = df.apply(lambda row: 1 if row['Response'] == row['Actuals'] else 0, axis=1)

# Proportion correct per participant
df['Proportion'] = df.groupby(['Participant_ID'])['Correct'].transform('mean')
df_proportions = df.drop_duplicates(subset=['Participant_ID'])[['Participant_ID', 'Experiment_Num', 'Proportion', 'Gender']]
df_proportions['Experiment_Num'] = df_proportions['Experiment_Num'].astype('category')


plt.figure(figsize=(12, 8), dpi=120)

# Violin plot 
sns.violinplot(
    x="Experiment_Num",
    y="Proportion",
    data=df_proportions,
    inner=None,
    color="#a8c1ff",
    linewidth=0,
)

boxplot_border_color = "#00164f"
# Boxplot
sns.boxplot(
    x="Experiment_Num",
    y="Proportion",
    data=df_proportions,
    width=0.16,
    color="#007AFF",
    boxprops={"edgecolor": boxplot_border_color, "zorder": 2},
    medianprops={"color": boxplot_border_color},
    whiskerprops={"color": boxplot_border_color},
    capprops={"color": boxplot_border_color},
)

# Data points
sns.stripplot(
    x="Experiment_Num",
    y="Proportion",
    data=df_proportions,
    color="#000000",
    alpha=0.6,
    jitter=True,
    zorder=4
)

# Mean
means = df_proportions.groupby('Experiment_Num')['Proportion'].mean()

for i, mean in enumerate(means):
    plt.hlines(mean, i - 0.08, i + 0.08, colors='#FFAE00', linestyles='dashed', linewidth=1.6, zorder=3)

plt.ylim(0.2, 0.8)
plt.title("Distribution of the proportion of correct responses across groups", fontsize=20)
plt.xlabel("Experiment Group", fontsize=20, fontweight="bold")
plt.ylabel("Proportion Correct", fontsize=20, fontweight="bold")
new_labels = ["Group 1:\nFull Body", "Group 2:\nBody Movements", "Group 3:\nFacial Features"]
plt.xticks(ticks=range(len(new_labels)), labels=new_labels, fontsize=16, color="#0055B2")
plt.yticks(fontsize=16, color="#0055B2")
plt.grid(color='#dbdbdb', linestyle='--', linewidth=0.7)
plt.show()