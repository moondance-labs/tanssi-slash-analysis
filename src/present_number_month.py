import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

def main():
    # Read the filtered CSV
    df = pd.read_csv('output/filtered_slashing.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Extract date and create month-year group
    df['Date'] = df['Time'].dt.date
    df['Month-Year'] = df['Time'].dt.strftime('%Y-%m')
    
    # Count slashes per day
    daily_counts = df.groupby('Date').size().reset_index(name='Slashes')
    
    # Set style and figure size
    plt.style.use('seaborn-v0_8')
    plt.figure(figsize=(12, 6))
    
    # Create the plot
    sns.lineplot(data=daily_counts, x='Date', y='Slashes')
    
    # Customize the plot
    plt.title('Daily Slashing Events', pad=20)
    plt.xlabel('Date')
    plt.ylabel('Number of Slashes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Create output directory if doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save the plot
    plt.savefig('output/slashing_trends.png')
    plt.close()

if __name__ == "__main__":
    main()