import sqlite3
import pandas as pd
import numpy as np
    
def get_full_dataset(conn):
    """
    Get complete dataset with all relevant features
    This joins all 3 tables and creates our analysis dataset
    """
    query = """
        SELECT 
            p.patient_id,
            p.age,
            p.gender,
            p.insurance_type,
            p.chronic_conditions,
            a.admission_id,
            a.length_of_stay,
            a.diagnosis_code,
            a.num_medications,
            a.num_procedures,
            r.readmitted_within_30_days,
            r.days_to_readmission
        FROM patients p
        JOIN admissions a ON p.patient_id = a.patient_id
        JOIN readmissions r ON a.admission_id = r.admission_id
    """
    
    df = pd.read_sql_query(query, conn)
    print(f"✓ Loaded {len(df)} admission records")
    return df

def get_summary_statistics(df):
    """Calculate summary statistics"""
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    
    print(f"\nTotal admissions: {len(df)}")
    print(f"Total unique patients: {df['patient_id'].nunique()}")
    print(f"Readmissions within 30 days: {df['readmitted_within_30_days'].sum()}")
    print(f"Overall readmission rate: {df['readmitted_within_30_days'].mean() * 100:.2f}%")
    
    print("\n" + "-"*60)
    print("Age Statistics:")
    print(df['age'].describe())
    
    print("\n" + "-"*60)
    print("Readmission Rate by Insurance Type:")
    readmission_by_insurance = df.groupby('insurance_type')['readmitted_within_30_days'].agg(['sum', 'count', 'mean'])
    readmission_by_insurance.columns = ['Readmissions', 'Total', 'Rate']
    readmission_by_insurance['Rate'] = readmission_by_insurance['Rate'] * 100
    print(readmission_by_insurance)
    
    return readmission_by_insurance


# Main
if __name__ == "__main__":

    conn = sqlite3.connect('data/hospital.db')

    # Get full dataset
    df = get_full_dataset(conn)
    
    # Display first few rows
    print("\n" + "="*60)
    print("SAMPLE DATA (First 5 rows)")
    print("="*60)
    print(df.head())
    
    # Get summary statistics
    summary = get_summary_statistics(df)
    
    # Save dataset to CSV for later use
    df.to_csv('data/analysis_dataset.csv', index=False)
    print("\n✓ Dataset saved to data/analysis_dataset.csv")
    
    # Close connection
    conn.close()