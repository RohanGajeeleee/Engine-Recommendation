from src.infrastructure.repositories.notification_repository import NotificationRepository
from src.infrastructure.repositories.feedback_repository import FeedbackRepository
import logging

class FeedbackRequestService:
    def __init__(self):
        self.notification_repository = NotificationRepository()
        self.feedback_repository = FeedbackRepository()

    def fetch_feedback_requests(self, employee_id):
        requests = self.notification_repository.get_feedback_requests(employee_id)
        if not requests:
            return "No feedback requests available."
        
        response = ""
        for request in requests:
            response += f"ID: {request['id']}, Message: {request['message']}\n"
        
        return response

    def reply_feedback_request(self, employee_id, request_id, menu_id, answer1, answer2, answer3):
        reply = f"Q1: {answer1}, Q2: {answer2}, Q3: {answer3}"
        feedback_reply = {
            'notification_id': request_id,
            'menu_id': menu_id,
            'employee_id': employee_id,
            'reply': reply
        }
        self.feedback_repository.save_feedback_reply(feedback_reply)
        return "Feedback request reply submitted successfully"
    
    def fetch_feedback_replies(self):
        replies = self.feedback_repository.get_feedback_replies()
        return replies
