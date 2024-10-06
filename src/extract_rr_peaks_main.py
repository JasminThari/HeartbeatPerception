import math   
import numpy as np   
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

#%% Segment the ECG signals into 10-second windows
fs = 2048
total_samples = len(ECG_data_dict[1])
segment_duration_sec = 10
segment_length = segment_duration_sec * fs
num_segments = int(np.ceil(total_samples / segment_length))

segment_boundaries = [
    (int(i * segment_length), int(min((i + 1) * segment_length, total_samples)))
    for i in range(num_segments)
]

peaks_segments_dict =  {key: {} for key in ECG_data_dict.keys()}
for i, (start, end) in enumerate(segment_boundaries):
    for key, peaks in peak_interpolated.items():
        peaks_in_segment = peaks[(peaks >= start) & (peaks < end)]
        peaks_in_seconds = peaks_in_segment / fs
        peaks_segments_dict[key][i] = {'peaks': peaks_in_segment, 'times': peaks_in_seconds}