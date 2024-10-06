import math   
import pandas as pd
import numpy as np   
import mne 
import heartpy as hp
import os

def bdf_loader(folder, seconds, chan1="EXG2-0", chan2="EXG2"):
    """
    Load ECG signals from BDF files in the specified folder.

    Parameters:
    - folder (str): Path to the folder containing BDF files.
    - seconds (int): Duration of the signal to extract in seconds.
    - chan1 (str): Primary channel name to extract.
    - chan2 (str): Secondary channel name to extract if chan1 is not found.

    Returns:
    - ecg_signals_dict (dict): Dictionary containing ECG signals for each subject.
    """
    
    ecg_signals_dict = {}
    
    for i in range(13):
        path = os.path.join(folder, f"sj{i+1}.bdf")
        
        temp = mne.io.read_raw_bdf(path, verbose='ERROR')

        # Get the index of the channel
        available_channels = temp.ch_names
        selected_channel = chan1 if chan1 in available_channels else chan2
        
        # Get the index of start and end of the signal
        temp_events = mne.find_events(temp, verbose='ERROR')  
        temp_start = temp_events[0, 0]
        temp_end = temp_start + int(temp.info['sfreq'] * seconds) 

        # Get the signal
        signal = temp.get_data(picks=selected_channel)[:, temp_start:temp_end]
        # Append to the dictionary
        ecg_signals_dict[i+1] = signal[0]
    
    return ecg_signals_dict

def apply_flip(ECG_data_dict, flip_flags):    
    flipped_ECG_data_dict = {}
    
    for (key, signal), flip in zip(ECG_data_dict.items(), flip_flags):
        if flip:
            signal_flipped = hp.flip_signal(signal, enhancepeaks=False, keep_range=True)
            flipped_ECG_data_dict[key] = signal_flipped  
        else:
            flipped_ECG_data_dict[key] = signal  
    
    return flipped_ECG_data_dict

def extract_RR_peaks(ECG_data_dict, sample_rate=2048):
    RR_Peaks_dict = {}   
    invalid_intervals_dict =  {key: {} for key in ECG_data_dict.keys()}
    peaks_dict = {}         

    for idx, (key, signal) in enumerate(ECG_data_dict.items()):
        # Process the signal to get peaks and measures
        peaks, m = hp.process(signal, sample_rate=sample_rate)
        RR_intervals_ms = peaks['RR_list']  
        peaklist = peaks['peaklist'][:-1]          

        # Store the RR intervals and peak indices in the dictionaries
        RR_Peaks_dict[key] = RR_intervals_ms
        peaks_dict[key] = peaklist

        # Find intervals outside the range [600, 1400] ms
        invalid_values = [rr for rr in RR_intervals_ms if rr < 600 or rr > 1400]
        invalid_mask = np.isin(RR_intervals_ms, invalid_values)
        invalid_intervals_dict[key]['mask'] = invalid_mask
        
        # If there are any invalid values, log them
        if invalid_values:
            invalid_intervals_dict[key]['invalid'] = invalid_values
            
    return RR_Peaks_dict, invalid_intervals_dict, peaks_dict
            
def interpolate_invalid_peaks(invalid_intervals_dict, peaks_dict):
    interpolated_peaks_dict = {}
    for subject in invalid_intervals_dict.keys():
        invalid_rrs = invalid_intervals_dict[subject]['mask']
        peak_interpolated_delete = np.delete(peaks_dict[subject], invalid_rrs)
        
        interpolated_peaks_dict[subject] = peak_interpolated_delete
    
    return interpolated_peaks_dict

def extract_rr_interpolated(peak_interpolated):
    interpolated_rr_intervals_dict = {}
    for key, peak_insert in peak_interpolated.items():
        interpolated_rr_intervals = hp.analysis.calc_rr(peak_insert, sample_rate=2048)
        interpolated_rr_intervals_dict[key] = interpolated_rr_intervals
    return interpolated_rr_intervals_dict