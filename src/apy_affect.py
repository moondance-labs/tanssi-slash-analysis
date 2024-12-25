import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def calculate_apy_impact(df):
    # Convert perbill fraction to percentage (1 billion = 100%)
    df['slash_percentage'] = (df['fraction'] / 1_000_000_000) * 100
    
    yearly_stats = df.groupby(df['Time'].dt.year).agg({
        'slash_percentage': ['count', 'sum', 'mean']
    }).round(4)
    
    yearly_stats.columns = ['Number_of_Slashes', 'Total_Percentage_Slashed', 'Average_Slash_Percentage']
    
    print("\nYearly Slashing Impact Analysis:")
    print("================================")
    for year, row in yearly_stats.iterrows():
        print(f"\nYear {year}:")
        print(f"Number of Slashes: {row['Number_of_Slashes']}")
        print(f"Total Stake Slashed: -{row['Total_Percentage_Slashed']}%")
        print(f"Average Slash Size: {row['Average_Slash_Percentage']}%")
        print(f"Effective Negative APY: -{row['Total_Percentage_Slashed']}%")
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=yearly_stats.index, y=yearly_stats['Total_Percentage_Slashed'])
    plt.title('Yearly Total Slashing Percentage (Negative APY Impact)')
    plt.xlabel('Year')
    plt.ylabel('Total Percentage Slashed (%)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    plt.savefig('output/yearly_slash_percentage.png')
    plt.close()

def main():
    df = pd.read_csv('output/filtered_slashing.csv')
    df['Time'] = pd.to_datetime(df['Time'])
    
    calculate_apy_impact(df)

if __name__ == "__main__":
    main()