import numpy as np
import matplotlib.pyplot as plt
import math

def plot_invalid_RR_segments(ECG_data_dict, RR_Peaks_dict, invalid_intervals, peaks_dict, sample_rate=2048):
    # Collect all invalid RR intervals into a list with associated keys and indices
    invalid_rr_info = []
    for key in invalid_intervals.keys():
        RR_intervals_ms = RR_Peaks_dict[key]
        invalid_rrs = invalid_intervals[key]['invalid']
        for invalid_rr in invalid_rrs:
            # Find all indices where the RR interval is invalid
            invalid_indices = [i for i, rr in enumerate(RR_intervals_ms) if rr == invalid_rr]
            for idx_invalid in invalid_indices:
                invalid_rr_info.append({'key': key, 'idx_invalid': idx_invalid})

    n_plots = len(invalid_rr_info)
    cols = 2
    rows = math.ceil(n_plots / cols)

    plt.figure(figsize=(15, 5 * rows))

    for i, info in enumerate(invalid_rr_info, 1):
        key = info['key']
        idx_invalid = info['idx_invalid']

        signal = ECG_data_dict[key]
        RR_intervals_ms = RR_Peaks_dict[key]
        peaklist = peaks_dict[key]

        # Determine the start and end indices for plotting
        start_idx = max(idx_invalid - 2, 0)
        end_idx = min(idx_invalid + 2, len(peaklist) - 1)

        # Get the indices of the two peaks surrounding the invalid RR interval
        peak1 = peaklist[start_idx]
        peak2 = peaklist[end_idx]

        # Extract the segment of the signal between peak1 and peak2
        segment = signal[peak1:peak2 + 1]

        # Create time vector for plotting
        t_segment = np.arange(peak1, peak2 + 1) / sample_rate

        # Plot the segment
        plt.subplot(rows, cols, i)
        plt.plot(t_segment, segment, label='ECG Signal')

        # Get the peaks in the segment
        peaks_in_segment = peaklist[start_idx:end_idx + 1]

        # Identify invalid peaks in the segment
        invalid_peaks = set()
        invalid_peaks.add(peaklist[idx_invalid])
        if idx_invalid + 1 < len(peaklist):
            invalid_peaks.add(peaklist[idx_invalid + 1])

        # Plot invalid peaks in red
        invalid_peaks_in_segment = [p for p in peaks_in_segment if p in invalid_peaks]
        t_invalid_peaks = [p / sample_rate for p in invalid_peaks_in_segment]
        amp_invalid_peaks = [signal[p] for p in invalid_peaks_in_segment]
        plt.scatter(t_invalid_peaks, amp_invalid_peaks, color='red', label='Invalid Peaks', zorder=5)

        # Plot valid peaks in green
        valid_peaks_in_segment = [p for p in peaks_in_segment if p not in invalid_peaks]
        t_valid_peaks = [p / sample_rate for p in valid_peaks_in_segment]
        amp_valid_peaks = [signal[p] for p in valid_peaks_in_segment]
        plt.scatter(t_valid_peaks, amp_valid_peaks, color='green', label='Valid Peaks', zorder=5)

        plt.title(f'Invalid RR Interval ({RR_intervals_ms[idx_invalid]:.2f} ms) for {key}')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()

    plt.tight_layout()
    plt.show()
