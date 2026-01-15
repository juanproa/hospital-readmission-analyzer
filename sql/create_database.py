# I think I just need to run this file once

import sqlite3


def create_database():
    """Create SQLite database with hospital tables"""
    
    # Connect to database (creates it if it doesn't exist (prob just needed for my first run))
    conn = sqlite3.connect('data/hospital.db')
    cursor = conn.cursor()
    
    # Create Patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            age INTEGER,
            gender TEXT,
            insurance_type TEXT,
            chronic_conditions INTEGER
        )
    ''')
    
    # Create Admissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admissions (
            admission_id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            admission_date DATE,
            discharge_date DATE,
            length_of_stay INTEGER,
            diagnosis_code TEXT,
            num_medications INTEGER,
            num_procedures INTEGER,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')
    
    # Create Readmissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readmissions (
            readmission_id INTEGER PRIMARY KEY,
            admission_id INTEGER,
            readmitted_within_30_days INTEGER,
            days_to_readmission INTEGER,
            FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
        )
    ''')
    
    conn.commit()
    print("✓ Database tables created successfully!")
    return conn

if __name__ == "__main__":
    conn = create_database()
    conn.close()