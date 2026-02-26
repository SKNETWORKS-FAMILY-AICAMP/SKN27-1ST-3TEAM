import csv
import pymysql
import os


db_config = {
    'host': 'localhost',
    'user': 'car_insert',       
    'password': 'car1234', 
    'db': 'car_insert', 
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_dir, 'FAQ_table_202602260908.csv')

try:
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) 

        sql = "INSERT INTO FAQ_table (FAQ_id, title, content, category) VALUES (%s, %s, %s, %s)"

        for row in reader:
            if row:
                cursor.execute(sql, row)

    conn.commit()
    print("MySQL 데이터 삽입 완료!")

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    if conn:
        conn.close()