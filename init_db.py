import os
import MySQLdb
from dotenv import load_dotenv

load_dotenv()

def init_db():
    connection = MySQLdb.connect(
        host=os.environ.get('MYSQL_HOST') or 'localhost',
        user=os.environ.get('MYSQL_USER') or 'root',
        password=os.environ.get('MYSQL_PASSWORD') or '',
    )
    cursor = connection.cursor()
    
    db_name = os.environ.get('MYSQL_DB') or 'pharmago'
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    
    
    schema_path = os.path.join(os.path.dirname(__file__), 'app', 'database.sql')
    with open(schema_path, 'r') as schema_file:
        schema = schema_file.read()
    
    
    for statement in schema.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()