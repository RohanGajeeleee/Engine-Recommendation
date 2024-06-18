import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from src.Database.db_config import get_db_connection

class Report:
    @staticmethod
    def generate_monthly_feedback_report(year, month):
        query = """
        SELECT 
            f.menu_id, 
            m.name AS menu_name, 
            f.comment, 
            f.rating, 
            f.feedback_date 
        FROM 
            feedback f
        JOIN 
            menu m ON f.menu_id = m.id
        WHERE 
            YEAR(f.feedback_date) = %s AND MONTH(f.feedback_date) = %s
        """
        results = Report._fetch_data(query, (year, month))

        if not results:
            print("No feedback found for the specified period.")
        else:
            Report._generate_and_save_report(results, year, month)

    @staticmethod
    def _fetch_data(query, params):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _generate_and_save_report(data, year, month):
        filename = f'monthly_feedback_report_{year}_{month}.csv'
        with open(filename, 'w') as file:
            file.write("Menu ID,Menu Name,Comment,Rating,Feedback Date\n")
            for row in data:
                file.write(f"{row['menu_id']},{row['menu_name']},{row['comment']},{row['rating']},{row['feedback_date']}\n")
        print(f"Report saved to {filename}")
        print("Monthly Feedback Report")
        for row in data:
            print(f"Menu ID: {row['menu_id']}, Menu Name: {row['menu_name']}, Comment: {row['comment']}, Rating: {row['rating']}, Date: {row['feedback_date']}")

if __name__ == "__main__":
    year = 2024
    month = 6
    Report.generate_monthly_feedback_report(year, month)
