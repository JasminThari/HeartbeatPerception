import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


file_path = 'Data/Results/results.csv'
data_raw = pd.read_csv(file_path)

experiment_1_data = data_raw[data_raw['Experiment_Num'] == 1]
experiment_2_data = data_raw[data_raw['Experiment_Num'] == 2]
experiment_3_data = data_raw[data_raw['Experiment_Num'] == 3]

def create_heatmap(data, experiment_num):
    heatmap_data = pd.DataFrame()

    for participant_id in data['Participant_ID'].unique():
        for pair_id in data['Pair_ID'].unique():
            match = data[(data['Participant_ID'] == participant_id) & (data['Pair_ID'] == pair_id)]
            if not match.empty:
                response_actuals_match = match['Response'].values[0] == match['Actuals'].values[0]
                heatmap_data.at[participant_id, pair_id] = 1 if response_actuals_match else 0
            else:
                heatmap_data.at[participant_id, pair_id] = 0

    # Reorder the heatmap data based on sorted indices
    correct_counts = heatmap_data.sum(axis=1)
    sorted_participants = correct_counts.sort_values(ascending=True).index

    pair_correct_counts = heatmap_data.sum(axis=0)
    sorted_pairs = pair_correct_counts.sort_values(ascending=False).index

    heatmap_data_sorted = heatmap_data.loc[sorted_participants, sorted_pairs]

    # average_correct_answers = correct_counts.mean()
    # print(f'Average correct answers for Experiment {experiment_num}: {average_correct_answers:.2f}')

    # Visualize the sorted heatmap
    plt.figure(figsize=(10, 3), dpi=200)

    cmap = sns.color_palette(["white", "black"])

    ax = sns.heatmap(heatmap_data_sorted,
                cmap=cmap,
                cbar=False,
                linewidths=0.4,
                linecolor='white', 
                square=True,
                annot=False)

    plt.xlabel('Pair #', fontsize=8, fontweight='bold')
    plt.ylabel('Participant ID', fontsize=8, fontweight='bold')

    ax.set_xticks(np.arange(len(sorted_pairs)) + 0.5)
    ax.set_xticklabels(sorted_pairs, rotation=70, ha='center', fontsize=6)

    ax.set_yticks(np.arange(len(sorted_participants)) + 0.5)
    ax.set_yticklabels(sorted_participants, fontsize=6, va='center')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    plt.show()

# For each experiment
create_heatmap(experiment_1_data, experiment_num=1)
# create_heatmap(experiment_2_data, experiment_num=2)
# create_heatmap(experiment_3_data, experiment_num=3)