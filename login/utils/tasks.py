from music.celery import app
from celery import Task
from celery.decorators import task

import boto3
import os


class AWS_SES(Task):
    
    def __init__(self, receivers, *args, **kwargs):
        self.client = boto3.client('ses')
        self.sender = 'lyoudr@gmail.com'
        self.receivers = receivers
        self.messages = {}


    def make_message(self, subject, text):
        self.messages = {
            'Subject': {
                'Data': subject, 
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': text,
                    'Charset': 'UTF-8'
                }
            }
        }
        return self.messages

    def send_mail(self, *args, **kwargs):
        self.client.send_email(
            Source = self.sender,
            Destination = {
                'ToAddresses' : self.receivers
            },
            Message = self.messages
        )

@app.task(name = 'send_email')
def send_email(email, token):
    print('email is =>', email)
    ses = AWS_SES([email])
    ses.make_message(
        'Music Reset Password Validation',
        f"""
            Email reset password, 
            Please refer to the following url to reset password : 
            {os.environ.get('EMAIL_WEB_HOST')}{token}
        """, 
    )
    ses.send_mail()
