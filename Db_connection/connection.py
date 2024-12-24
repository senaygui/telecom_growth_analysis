import pandas as pd
import psycopg2
from sqlalchemy import create_engine

class PostgresConnection:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL database!")
        except Exception as e:
            print(f"Error: {e}")
    def write_dataframe_to_db(self, df, table_name):
        try:
        # Create SQLAlchemy engine using the connection parameters from the PostgresConnection class
            engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')
        
        # Write DataFrame to SQL table, replacing if the table already exists
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Data successfully written to table {table_name}.")
        except Exception as e:
            print(f"Error writing DataFrame to table: {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("Connection closed.")
            

db = PostgresConnection(dbname='telecom', user='postgres', password='postgres')
db.connect()


query = "SELECT * FROM xdr_data"
result = db.execute_query(query)


df = pd.DataFrame(result, columns=[desc[0] for desc in db.cursor.description])

db.close_connection()