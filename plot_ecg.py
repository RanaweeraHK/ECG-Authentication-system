import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

# plot the ecg_signal

data_dir = 'Data/Signals'

def original_ecg_signal(data_dir , file_path):
    signal_csv_path = os.path.join(data_dir, file_path)
    signal_df = pd.read_csv(signal_csv_path)

    max_time = 2
    signal_df  = signal_df[signal_df['time'] < max_time]

    plt.figure(figsize=(10, 6))

    # Plot each signal column except 'time'
    for column in signal_df.columns:
        if column != 'time':
            plt.plot(signal_df['time'], signal_df[column], label=column)

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('{} ECG Signal'.format(file_path.split('_')[0]))
    plt.legend()
    plt.show()


record_names =  [f'{i:03d}' for i in range(100, 235)]
existing_records = [i for i in record_names if f'{i}_signal.csv' in os.listdir(data_dir)]

def all_ecg_signal(ax, data_dir, file_path):
    signal_csv_path = os.path.join(data_dir, file_path)
    signal_df = pd.read_csv(signal_csv_path)

    max_time = 2
    signal_df = signal_df[signal_df['time'] < max_time]

    for column in signal_df.columns:
        if column != 'time':
            ax.plot(signal_df['time'], signal_df[column], label=column)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('{} ECG Signal'.format(file_path.split('_')[0]))
    ax.legend()

num_rows = (len(existing_records) + 2) // 3
fig, axs = plt.subplots(num_rows, 3, figsize=(10, 6 * num_rows))

for i, record_name in enumerate(existing_records):
    row_idx = i // 3
    col_idx = i % 3

    all_ecg_signal(axs[row_idx, col_idx], data_dir, f'{record_name}_signal.csv')

plt.tight_layout()
plt.show()

