from db_config import get_db_connection

db = get_db_connection()
cursor = db.cursor()

cursor.execute("SHOW TABLES")
print(cursor.fetchall())

cursor.close()
db.close()