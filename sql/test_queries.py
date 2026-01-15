import sqlite3
import pandas as pd

def run_query(query, description):
    """Execute a SQL query and display results"""
    conn = sqlite3.connect('data/hospital.db')
    # print(f"\n{'='*60}")
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    df = pd.read_sql_query(query, conn)
    print(df)
    
    conn.close()
    return df

# Test your queries here
if __name__ == "__main__":
    
    # # Query 1: Total patients
    # query1 = """
    # SELECT COUNT(*) as total_patients
    # FROM patients
    # """
    # run_query(query1, "Query 1: Total Patients")
    
    # # Query 2: Average Age by Gender
    # query2 = """
    # SELECT gender, AVG(age) as average_age
    # FROM patients
    # GROUP BY gender
    # """
    # run_query(query2, "Query 2: Average Age by Gender")

    # # Query 3: Top 5 most common diagnosis codes
    # query3 = """
    # SELECT diagnosis_code, COUNT(*) AS diagnosis_count
    # FROM admissions
    # GROUP BY diagnosis_code
    # ORDER BY diagnosis_count DESC  
    # LIMIT 5
    # """
    # run_query(query3, "Query 3: Top 5 most common diagnosis codes")

    # # # Query 4: Patients Readmitted Within 30 Days
    # query4 = """
    # SELECT p.patient_id, p.age, r.days_to_readmission
    # FROM patients p 
    # JOIN admissions a ON p.patient_id = a.patient_id 
    # JOIN readmissions r ON a.admission_id = r.admission_id
    # WHERE r.readmitted_within_30_days = 1
    # """
    # run_query(query4, "Query 4: Patients Readmitted Within 30 Days")

    # # Query 5: Calculate readmission rate by insurance type
    query5 = """
    SELECT p.insurance_type, 
           COUNT(a.admission_id) AS total_admissions,
           SUM(r.readmitted_within_30_days) AS readmissions,
           ROUND((SUM(r.readmitted_within_30_days) * 100.0 / COUNT(a.admission_id)), 2) || '%' AS readmission_rate
    FROM patients p
    JOIN admissions a ON p.patient_id = a.patient_id 
    JOIN readmissions r ON a.admission_id = r.admission_id
    GROUP BY p.insurance_type
    """
    run_query(query5, "Query 5: Calculate readmission rate by insurance type")