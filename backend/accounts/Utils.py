from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list, from_email=None, fail_silently=False):
    """
    Utility function to send an email using Django's built-in email functionality.
    
    Args:
    - subject (str): The subject of the email.
    - message (str): The body of the email.
    - recipient_list (list): A list of recipient email addresses.
    - from_email (str, optional): The sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.
    - fail_silently (bool, optional): Whether to suppress errors. Defaults to False.
    
    Returns:
    - int: The number of successfully delivered messages.
    """
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER
    
    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=fail_silently,
    )
