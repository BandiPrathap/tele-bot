import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="bk9e88trktdw7imnmxnw-mysql.services.clever-cloud.com",
            user="us8fpwzkjnzfdcxa",
            password="E9EKCLspQW1QSXE4pXJ",
            database="bk9e88trktdw7imnmxnw"
        )
        if connection.is_connected():
            print("Successfully connected to MySQL")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
connect_to_db()