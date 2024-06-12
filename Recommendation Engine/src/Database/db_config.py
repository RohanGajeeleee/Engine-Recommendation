import mysql.connector
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pranav04",
            database="cafeteria"
        )
        return db
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        raise
