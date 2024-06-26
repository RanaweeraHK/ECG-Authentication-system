import os
import pandas as pd
import numpy as np
import neurokit2 as nk
from sklearn.preprocessing import MinMaxScaler


def ecg_clean(data_dir, file_path):
    signal_csv_path = os.path.join(data_dir, file_path)
    signal_df = pd.read_csv(signal_csv_path)
    
    ecg_signal = signal_df['signal_0'].values
    ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=360)
    
    signal_df['signal_0_clean'] = ecg_cleaned
    
    signal_df.to_csv(signal_csv_path, index=False)
    return signal_df

def normalize_ecg_signal(ecg_signal):
    scaler = MinMaxScaler()
    ecg_signal_normalized = scaler.fit_transform(ecg_signal.reshape(-1, 1))
    return ecg_signal_normalized.flatten()

def add_normalized_signal(data_dir, file_path):
    signal_csv_path = os.path.join(data_dir, file_path)
    signal_df = pd.read_csv(signal_csv_path)
    
    ecg_cleaned = signal_df['signal_0_clean'].values
    ecg_cleaned_norm = normalize_ecg_signal(ecg_cleaned)
    
    signal_df['signal_0_clean_norm'] = ecg_cleaned_norm
    signal_df.to_csv(signal_csv_path, index=False)
    return signal_df

data_dir = 'Data/Signals'
record_names =  [f'{i:03d}' for i in range(100, 235)]
existing_records = [i for i in record_names if f'{i}_signal.csv' in os.listdir(data_dir)]

for record_name in existing_records:
    file_path = f'{record_name}_signal.csv'
    ecg_clean(data_dir, file_path)
    add_normalized_signal(data_dir, file_path)





