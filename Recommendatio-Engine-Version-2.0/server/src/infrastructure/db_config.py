import mysql.connector

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
        
        raise

