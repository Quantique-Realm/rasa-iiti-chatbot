import psycopg2

try:
    conn = psycopg2.connect(
        dbname="IITI_Bot_Queries",  # Use your actual database name
        user="postgres",  # Use your actual PostgreSQL username
        password="HBX814",  # Replace with your actual password
        host="localhost",  # Change if using a remote database
        port="5432"  # Default PostgreSQL port
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Error connecting to database:", e)