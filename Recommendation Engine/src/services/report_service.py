from src.models.reporting import Report

class ReportService:
    @staticmethod
    def generate_report():
        year = int(input("Enter year: "))
        month = int(input("Enter month: "))
        Report.generate_monthly_feedback_report(year, month)
        return True
