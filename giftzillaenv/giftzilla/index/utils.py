# views.py or wherever you want to send emails

from django.core.mail import send_mail

def send_email(subject, message, recipient_list):
    
    from_email = 'noreply.giftzilla@gmail.com'

    send_mail(subject, message, from_email, recipient_list)

    return "success"
