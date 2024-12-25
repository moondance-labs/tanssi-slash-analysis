import os
import pandas as pd
from datetime import datetime, timedelta

def parse_time_ago(time_str, current_time):
    parts = time_str.strip().split()
    delta = timedelta()
    for i in range(0, len(parts) - 1, 2):
        value = int(parts[i])
        unit = parts[i + 1]
        if 'day' in unit:
            delta += timedelta(days=value)
        elif 'hr' in unit:
            delta += timedelta(hours=value)
    return current_time - delta

def process_file(filepath, current_time):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    records = []
    current_record = None
    i = 6  # Skip header lines
    
    while i < len(lines):
        line = lines[i]
        if 'CopyCopy LinkView code' in line:
            if current_record:
                records.append(current_record)
            current_record = None
        elif line and '\t' in line:  # Event ID, Block, Extrinsic ID line
            current_record = {}
            parts = line.split('\t')
            current_record['Event ID'] = parts[0]
            current_record['Block'] = parts[1]
            current_record['Extrinsic ID'] = parts[2]
        elif 'ago' in line:
            current_record['Time'] = parse_time_ago(line, current_time).strftime('%Y-%m-%dT%H:%M')
        elif 'staking' in line:
            current_record['Type'] = line.strip()
        elif (line == 'validator' or line == 'AccountId') and i + 1 < len(lines):
            current_record['validator'] = lines[i + 1]
            i += 1
        elif (line == 'fraction' or line == 'Perbill') and i + 1 < len(lines):
            current_record['fraction'] = int(lines[i + 1])
            i += 1
        elif (line == 'slash_era' or line == 'EraIndex') and i + 1 < len(lines):
            current_record['slash_era'] = int(lines[i + 1])
            i += 1
        i += 1
    
    return records

def main():
    current_time = datetime.fromisoformat('2024-12-24T18:14')
    data_dir = 'data'
    all_records = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            records = process_file(filepath, current_time)
            all_records.extend(records)
    
    df = pd.DataFrame(all_records)
    df.to_csv('output/slashing_data.csv', index=False)

if __name__ == "__main__":
    main()