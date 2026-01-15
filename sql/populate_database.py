import sqlite3
import random
from datetime import datetime, timedelta

def generate_sample_data(conn, num_patients=1000):
    """Generate realistic sample hospital data"""
    cursor = conn.cursor()
    
    # Sample data lists
    genders = ['M', 'F']
    insurance_types = ['Medicare', 'Medicaid', 'Private', 'Self-Pay']
    diagnosis_codes = ['I50.9', 'J44.1', 'E11.9', 'I10', 'N18.9', 
                       'J18.9', 'I48.91', 'K92.2', 'E87.6', 'I25.10']
    
    print("Generating patient data...")
    # Generate patients
    patients = []
    for i in range(1, num_patients + 1):
        age = random.randint(18, 95)
        gender = random.choice(genders)
        insurance = random.choice(insurance_types)
        chronic_conditions = random.choices([0, 1, 2, 3, 4, 5], 
                                           weights=[10, 25, 30, 20, 10, 5])[0]
        patients.append((i, age, gender, insurance, chronic_conditions))
    
    cursor.executemany('''
        INSERT INTO patients VALUES (?, ?, ?, ?, ?)
    ''', patients)
    
    print("Generating admission data...")
    # Generate admissions
    admissions = []
    admission_id = 1
    start_date = datetime(2023, 1, 1)
    
    for patient_id in range(1, num_patients + 1):
        # Each patient has 1-3 admissions
        num_admissions = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        
        for _ in range(num_admissions):
            admission_date = start_date + timedelta(days=random.randint(0, 700))
            length_of_stay = random.choices(range(1, 16), 
                                           weights=[20, 15, 12, 10, 8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1])[0]
            discharge_date = admission_date + timedelta(days=length_of_stay)
            diagnosis_codes = random.choice(diagnosis_codes)
            num_medications = random.randint(1, 12)
            num_procedures = random.randint(0, 5)
            
            admissions.append((admission_id, patient_id, 
                             admission_date.strftime('%Y-%m-%d'),
                             discharge_date.strftime('%Y-%m-%d'),
                             length_of_stay, diagnosis_codes, 
                             num_medications, num_procedures))
            admission_id += 1
    
    cursor.executemany('''
        INSERT INTO admissions VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', admissions)
    
    print("Generating readmission data...")
    # Generate readmissions
    readmissions = []
    for admission_id in range(1, len(admissions) + 1):
        # 25% chance of readmission within 30 days
        readmitted = 1 if random.random() < 0.25 else 0
        days_to_readmission = random.randint(1, 30) if readmitted else None
        
        readmissions.append((admission_id, admission_id, readmitted, days_to_readmission))
    
    cursor.executemany('''
        INSERT INTO readmissions VALUES (?, ?, ?, ?)
    ''', readmissions)
    
    conn.commit()
    print(f"✓ Generated data for {num_patients} patients!")
    print(f"✓ Total admissions: {len(admissions)}")
    print(f"✓ Total readmissions tracked: {len(readmissions)}")

if __name__ == "__main__":
    conn = sqlite3.connect('data/hospital.db')
    generate_sample_data(conn, num_patients=1000)
    conn.close()
    print("\n✓ Database populated successfully!")