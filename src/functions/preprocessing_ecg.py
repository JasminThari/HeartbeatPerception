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