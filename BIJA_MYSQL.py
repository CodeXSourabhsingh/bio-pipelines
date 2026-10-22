
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=3
    )

def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bija_report (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mode VARCHAR(20),
                male_education TEXT,
                female_education TEXT,
                both_education TEXT,
                calculation_result VARCHAR(255),
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Table 'bija_report' created successfully.")
    except Exception as e:
        print(f"❌ Error creating table: {e}")

def insert_report(mode, male_edu=None, female_edu=None, both_edu=None, calc_result=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO bija_report (mode, male_education, female_education, both_education, calculation_result)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (mode, male_edu, female_edu, both_edu, calc_result))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Data inserted successfully.")
        return True
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

if __name__ == "__main__":
    create_table()