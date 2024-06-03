from src.db_config.py import get_db_connection

def authenticate_user(employee_id, name):
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT role FROM users WHERE employee_id = %s AND name = %s"
    cursor.execute(query, (employee_id, name))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result:
        return result[0]  # Return the role of the user
    return None

if __name__ == "__main__":
    role = authenticate_user('E123', 'John Doe')
    if role:
        print(f"Authenticated as {role}")
    else:
        print("Authentication failed")
