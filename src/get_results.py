#%% import libraries
import os
import pandas as pd
from sklearn.metrics import accuracy_score

#%% Get results
folder_path = '../Data/Answers'

dataframes = []
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        filename_list = filename.split('_')
        participant_id = filename_list[4]
        experiment_num = filename_list[2]
        gender = filename_list[7].replace('.csv', '')
        
        file_path = os.path.join(folder_path, filename)
        print(f'Processing {file_path}')
        df = pd.read_csv(file_path)
        df['trial_num'] = df.index + 1
        df.rename(columns={'Video': 'ID'}, inplace=True)
        
        # Add metadata
        df['Participant_ID'] = participant_id
        df['Participant_ID'] = df['Participant_ID'].astype(int)
        df['Experiment_Num'] = experiment_num
        df['Gender'] = gender.lower()
        
        dataframes.append(df)

results_df = pd.concat(dataframes, ignore_index=True)

#%% Get actual
df_actuals = pd.read_csv('assignments/final_assignment_with_peaks.csv')
df_actuals['Actuals'] = df_actuals.apply(lambda row: 'left' if row['HeartBeat'] == row['Left'] else 'right', axis=1)

# %% Merge results and actuals
df_results = pd.merge(df_actuals, results_df, on='ID')
df_results.rename(columns={'ID': 'Pair_ID'}, inplace=True)

#%% 
cols = ['Participant_ID', 'trial_num', 'Gender', 'Experiment_Num', 'Pair_ID', 'Response', 'Actuals', 'Participant_x', 'Segment_x', 'Participant_y', 'Segment_y', 'Left',
       'Right', 'HeartBeat', 'Stimuli_Seconds', 'Peaks_Idx', 'Peaks_Seconds']
df_results = df_results[cols]
df_results.sort_values(by=['Participant_ID'], inplace=True, ignore_index=True)

#%% save results
df_results.to_csv('../Data/Results/results.csv', index=False)
# %%
