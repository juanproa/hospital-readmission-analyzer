import pandas as pd
import matplotlib.pyplot as plt

def plot_readmission_by_insurance(df):
    """Bar chart of readmission rates by insurance type"""
    
    insurance_rate_stats = df.groupby('insurance_type')['readmitted_within_30_days'].mean() * 100
    
    plt.figure(figsize=(10, 6))
    insurance_rate_stats.plot(kind='bar', color='black')
    
    plt.title('30-Day Readmission Rate by Insurance Type')
    plt.xlabel('Insurance Type')
    plt.ylabel('Readmission Rate (%)')
    plt.xticks(rotation=45) # Looks better this way
    plt.savefig('visualizations/readmission_by_insurance.png', dpi=300)
    print("✓ Saved: readmission_by_insurance.png")
    plt.close()


def plot_age_distribution(df):
    """Age comparison: readmitted vs not readmitted"""

    not_readmitted = df[df['readmitted_within_30_days'] == 0]['age']
    readmitted = df[df['readmitted_within_30_days'] == 1]['age']
    
    plt.figure(figsize=(10, 6))
    plt.hist(not_readmitted, bins=20, alpha=0.6, label='Not Readmitted', color='green')
    plt.hist(readmitted, bins=20, alpha=0.6, label='Readmitted', color='red')
    
    plt.title('Age Distribution: Readmitted vs Not Readmitted')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.legend()
    plt.savefig('visualizations/age_distribution.png', dpi=300)
    print("✓ Saved: age_distribution.png")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv('data/analysis_dataset.csv')
    print(f"Creating visualizations for {len(df)} records...\n")
    
    plot_readmission_by_insurance(df)
    plot_age_distribution(df)
    
    print("\n✓ Done! Check visualizations/ folder")