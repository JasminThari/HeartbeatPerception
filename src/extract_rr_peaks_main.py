#%% Import libraries
import math   
import numpy as np
import pandas as pd 
import mne 
import heartpy as hp
import os
from functions.preprocessing_ecg import bdf_loader, apply_flip, extract_RR_peaks, interpolate_invalid_peaks, extract_rr_interpolated

#%% Load ECG signals from BDF files
folder = "../Data/ECG_Signals"
ECG_data_dict = bdf_loader(folder, 120)

#%% Apply flip to ECG signals
flip_signal = [False, True, False, True, False, False, False, True, True, False,
              False, False, False]
ECG_data_preproccesed_dict = apply_flip(ECG_data_dict, flip_signal) 

#%% Extract RR peaks from ECG signals and interpolate invalid peaks
RR_Peaks_dict, invalid_intervals_dict, peaks_dict = extract_RR_peaks(ECG_data_preproccesed_dict)

# interpolate invalid peaks
peak_interpolated = interpolate_invalid_peaks(invalid_intervals_dict, peaks_dict) # the peaks
interpolated_rr_intervals_dict = extract_rr_interpolated(peak_interpolated) # the RR intervals

#%% extract segments
final_assignments = pd.read_csv('assignments/final_assignment.csv')

def extract_segments(df):
    heartbeat_segments = {}

    for _, row in df.iterrows():
        heartbeat = row['HeartBeat']
        # Check if HeartBeat matches Participant_x or Participant_y
        if heartbeat == row['Participant_x']:
            segment = row['Segment_x']
        elif heartbeat == row['Participant_y']:
            segment = row['Segment_y']
        else:
            segment = None  # In case there is no match, though it shouldn't happen in your data

        # Add the segment to the dictionary, grouped by heartbeat
        if heartbeat in heartbeat_segments:
            heartbeat_segments[heartbeat].append(segment)
        else:
            heartbeat_segments[heartbeat] = [segment]
    
    return heartbeat_segments

heartbeat_segments = extract_segments(final_assignments)

#%% Segment the ECG signals into 10-second windows
fs = 2048
segment_duration_sec = 10
segment_length = segment_duration_sec * fs

# Peaks dictionary to store peaks for each segment
peaks_segments_dict = {key: {} for key in ECG_data_dict.keys()}

# Loop through each person and their segments
for person, segments in heartbeat_segments.items():
    total_samples = len(ECG_data_dict[person])
    for segment_start_sec in segments:
        # Adjust the start of the segment by adding 10 seconds
        start_sec = segment_start_sec
        end_sec = start_sec + segment_duration_sec
        
        # Convert start and end times to sample indices
        start_sample = int(start_sec * fs)
        end_sample = int(end_sec * fs)
        
        # Ensure we don't exceed total samples
        end_sample = min(end_sample, total_samples)
        
        # Extract peaks in this adjusted segment for this person
        peaks_in_segment = peak_interpolated[person][(peak_interpolated[person] >= start_sample) & (peak_interpolated[person] < end_sample)]
        peaks_in_seconds = peaks_in_segment / fs
        # Adjust the times to range from 0 to 10 seconds
        adjusted_peaks_in_seconds = peaks_in_seconds- segment_start_sec
        
        # Store the results
        if person not in peaks_segments_dict:
            peaks_segments_dict[person] = {}
        

        
        peaks_segments_dict[person][segment_start_sec] = {'peaks': peaks_in_segment, 'seconds': peaks_in_seconds, 'adjusted_seconds': adjusted_peaks_in_seconds}

#%% Save the RR peaks for each segment
def get_heart_peaks(row, peaks_segments_dict):
    heartbeat = row['HeartBeat']
    
    # Determine which segment to use based on HeartBeat match
    if heartbeat == row['Participant_x']:
        segment = row['Segment_x']
    elif heartbeat == row['Participant_y']:
        segment = row['Segment_y']
    else:
        return None  
    
    # Get the peaks from the dictionary
    if heartbeat in peaks_segments_dict:
        return {
            'adjusted_seconds': peaks_segments_dict[heartbeat].get(segment, {}).get('adjusted_seconds', []),
            'peaks': peaks_segments_dict[heartbeat].get(segment, {}).get('peaks', []), 
            'seconds': peaks_segments_dict[heartbeat].get(segment, {}).get('seconds', [])
        }
    return []

# Apply the function to each row of the dataframe
final_assignments['Stimuli_Seconds'] = final_assignments.apply(lambda row: get_heart_peaks(row, peaks_segments_dict).get('adjusted_seconds', []), axis=1)
final_assignments['Peaks_Idx'] = final_assignments.apply(lambda row: get_heart_peaks(row, peaks_segments_dict).get('peaks', []), axis=1)
final_assignments['Peaks_Seconds'] = final_assignments.apply(lambda row: get_heart_peaks(row, peaks_segments_dict).get('seconds', []), axis=1)
#%%
final_assignments['ID'] = final_assignments.apply(lambda row: f"Pair_{row.name + 1}", axis=1)
final_assignments.to_csv('assignments/final_assignment_with_peaks.csv', index=False)
# %%
