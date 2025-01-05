import psycopg2
import pandas as pd
from psycopg2 import sql
from psycopg2 import OperationalError
from psycopg2 import sql,OperationalError
from sqlalchemy import create_engine

def check_table_exists(cursor, table_name):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'raw_tables' AND table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]

def load_data_to_postgres(filepath, table_name):
    try:
        # الاتصال بقاعدة البيانات
        conn = psycopg2.connect(
            dbname="project_DB", 
            user="postgres", 
            password="123", 
            host="localhost", 
            port="5432"
        )

        # إنشاء كائن cursor
        cursor = conn.cursor()

        # التحقق من وجود الجدول في قاعدة البيانات
        if not check_table_exists(cursor, table_name):
            print(f"Error: The table '{table_name}' does not exist in 'raw_tables' schema.")
            return

        # قراءة البيانات من الملف CSV
        data = pd.read_csv(filepath)
        columns = list(data.columns)

        # بناء استعلام INSERT مع placeholder
        insert_query = sql.SQL("INSERT INTO raw_tables.{} ({}) VALUES ({})").format(
            sql.Identifier(table_name),  # تخصيص اسم الجدول
            sql.SQL(', ').join(map(sql.Identifier, columns)),  # تخصيص الأعمدة
            sql.SQL(', ').join([sql.Placeholder()] * len(columns))  # تخصيص القيم
        )

        # إدخال البيانات إلى قاعدة البيانات
        for row in data.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)

        # تأكيد التغييرات في قاعدة البيانات
        conn.commit()

        print("Data loaded successfully!")

    except pd.errors.EmptyDataError:
        print(f"Error: The file '{filepath}' is empty")

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found")

    except OperationalError as e:
        print(f"Operational error while loading data into table '{table_name}': {e}")
    
    except Exception as e:
        print(f"An error occurred while loading data into table '{table_name}': {e}")

if __name__ == "__main__":
    try:
        load_data_to_postgres(r"C:/Users/Ahmed/Desktop/project/dataWH_clean/customersData.csv", "customersData")
        load_data_to_postgres(r"C:/Users/Ahmed/Desktop/project/dataWH_clean/salesData.csv", "salesData")
    except Exception as e:
        print(f"A critical error occurred: {e}")
