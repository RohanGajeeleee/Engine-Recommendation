import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
import pandas as pd
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

        df = pd.DataFrame(results)
        if Report._is_dataframe_empty(df):
            print("No feedback found for the specified period.")
        else:
            Report._generate_and_save_report(df, year, month)

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
    def _is_dataframe_empty(df):
        return df.empty

    @staticmethod
    def _generate_and_save_report(df, year, month):
        print("Monthly Feedback Report")
        print(df)
        df.to_csv(f'monthly_feedback_report_{year}_{month}.csv', index=False)
        print(f"Report saved to monthly_feedback_report_{year}_{month}.csv")
