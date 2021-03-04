from django.core.mail import send_mail

from celery.decorators import task
from celery.utils.log import get_task_logger


@task(name = 'send_email')
def send_email(subject, message, from_email, to_email, html_msg):
    logger = get_task_logger(__name__)
    logger.info('Sent email')
    send_mail(
        subject = subject,  
        message = message,
        from_email = from_email,
        recipient_list = [to_email],
        fail_silently=False,
        html_message= html_msg
    )
