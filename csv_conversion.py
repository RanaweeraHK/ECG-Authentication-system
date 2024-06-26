import os
import pandas as pd
import numpy as np
import wfdb

dir_path = 'mit-bih-arrhythmia-database-1.0.0'

# Extract patient info from header files
def read_header(file_path):
    # path = os.path.join(file_path)
    with open(file_path) as f:
        header_lines = f.readlines()
    details =[line.strip().split() for line in header_lines if line.startswith('#')]
    patient_info ={}
    patient_info['Age'] = details[0][1]
    patient_info['Gender'] = details[0][2]
    patient_info['ECG_params'] = ' '.join(details[0][3:])
    patient_info['Diagnoses'] = ' '.join(details[1][1:])

    flatten_details = [item.replace('#', '').strip() for sublist in details[2:] for item in sublist]
    patient_info['other'] = ' '.join(flatten_details)

    for key,value in patient_info.items():
        if len(value) == 0:
            patient_info[key] = 'NaN'
    return patient_info


def convert_record_to_csv(record_name, output_dir='Data'):
    record_path = os.path.join(dir_path, record_name)
    
    signal = wfdb.rdrecord(record_path)
    annotation = wfdb.rdann(record_path, 'atr')
    
    signal_df = pd.DataFrame(signal.p_signal, columns=[f'signal_{i}' for i in range(signal.p_signal.shape[1])])
    signal_df['time'] = signal_df.index / signal.fs
    
    annotation_df = pd.DataFrame({
        'time': annotation.sample / signal.fs, 
        'annotation': annotation.symbol
    })


    signal_csv_path = os.path.join(output_dir,'Signals', f'{record_name}_signal.csv')
    annotation_csv_path = os.path.join(output_dir, 'Annotations' ,f'{record_name}_annotations.csv')
    
    signal_df.to_csv(signal_csv_path, index=False)
    annotation_df.to_csv(annotation_csv_path, index=False)
    
    header_file_path = f'{record_path}.hea'
    patient_info = read_header(header_file_path)
    patient_info_df = pd.DataFrame([patient_info])
    patient_info_csv_path = os.path.join(output_dir, 'Patients',f'{record_name}_patient_info.csv')
    patient_info_df.to_csv(patient_info_csv_path, index=False)



dir_path = 'mit-bih-arrhythmia-database-1.0.0'
output_dir = 'Data'
os.makedirs(output_dir, exist_ok=True)

record_names = [f'{i:03d}' for i in range(100, 235)]

for record_name in record_names:
    try:
        convert_record_to_csv(record_name, output_dir)
    except FileNotFoundError as e:
        continue
print('Done')