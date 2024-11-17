import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLDatabase:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute_select(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_insert(self, query, values):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
