# Description: This script is used to initialize the database.
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="gym_rpg",
        user='admin',
        password='admin',
        port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()
conn.commit()
cur.close()
conn.close()
