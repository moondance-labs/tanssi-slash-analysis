import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

def main():
    df = pd.read_csv('output/filtered_slashing.csv')
    df['Time'] = pd.to_datetime(df['Time'])
    df['Date'] = df['Time'].dt.date
    
    # Count and calculate cumulative sum
    daily_counts = df.groupby('Date').size().reset_index(name='Daily_Slashes')
    daily_counts['Cumulative_Slashes'] = daily_counts['Daily_Slashes'].cumsum()
    
    plt.style.use('seaborn-v0_8')
    plt.figure(figsize=(12, 6))
    
    sns.lineplot(data=daily_counts, x='Date', y='Cumulative_Slashes', linewidth=2)
    
    plt.title('Cumulative Slashing Events Over Time', pad=20)
    plt.xlabel('Date')
    plt.ylabel('Total Number of Slashes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    os.makedirs('output', exist_ok=True)
    plt.savefig('output/cumulative_slashing_trends.png')
    plt.close()

if __name__ == "__main__":
    main()