import pandas as pd
import os

def main():
    # Read the CSV file
    df = pd.read_csv('output/slashing_data.csv')
    
    # Sort by Time to keep the earliest slashing event
    df = df.sort_values('Time')
    
    # Drop duplicates based on validator and slash_era, keeping first occurrence
    df_filtered = df.drop_duplicates(subset=['validator', 'slash_era'], keep='first')
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save filtered data
    df_filtered.to_csv('output/filtered_slashing.csv', index=False)

if __name__ == "__main__":
    main()