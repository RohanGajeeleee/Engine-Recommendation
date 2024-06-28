from src.infrastructure.repositories.notification_repository import NotificationRepository
from src.infrastructure.repositories.feedback_repository import FeedbackRepository
import logging
class FeedbackRequestService:
    @staticmethod
    def fetch_feedback_requests(employee_id):
        requests = NotificationRepository.get_feedback_requests(employee_id)
        if not requests:
            return "No feedback requests available."
        
        response = ""
        for request in requests:
            response += f"ID: {request['id']}, Message: {request['message']}\n"
        
        return response

    
    @staticmethod
    def reply_feedback_request(employee_id, request_id, menu_id, answer1, answer2, answer3):
        reply = f"Q1: {answer1}, Q2: {answer2}, Q3: {answer3}"
        feedback_reply = {
            'notification_id': request_id,
            'menu_id': menu_id,
            'employee_id': employee_id,
            'reply': reply
        }
        FeedbackRepository.save_feedback_reply(feedback_reply)
        return "Feedback request reply submitted successfully"
    
    @staticmethod
    def fetch_feedback_replies():
        replies = FeedbackRepository.get_feedback_replies()
        return replies