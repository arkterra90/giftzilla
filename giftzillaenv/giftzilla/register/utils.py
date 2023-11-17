import random
import string
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.sites.shortcuts import get_current_site




from .models import emailVerify, User


def generate_pin():
    while True:
        # Generate a random 5-character alphanumeric PIN (uppercase letters and numbers)
        characters = string.ascii_uppercase + string.digits +string.ascii_lowercase
        random_pin = ''.join(random.choice(characters) for _ in range(5))

        # Check if the PIN is already used
        if not emailVerify.objects.filter(pin=random_pin).exists():
            return(random_pin)
        
def send_verify(emailPin, userID, request):
    
    email_verify_url = reverse('register:email_Verify', args=[userID, emailPin])
    current_site = get_current_site(request)
    full_url = f"http://{current_site.domain}{email_verify_url}"

    print(full_url)

    user = User.objects.get(id=userID)

    html_message = format_html(
        f"Hello {user.first_name} {user.last_name},<br>"
        f"You have registered for a new account with GiftZilla. Please click the link below to<br>"
        f"verify your email and activate your account.<br>"
        f"<a href='{full_url}'>Activate Account</a><br>"
        "<br>"
        "Thanks, <br>"
        "GiftZilla"
    )    

    subject = "GiftZilla: Your registry pairing is READY!"
    message = f" { user.first_name }, You have created a new account with GiftZilla please click the link to verify account {email_verify_url}."
    emailVer = send_mail(subject, message=html_message, recipient_list=[user.email], from_email='noreply.giftzilla@gmail.com', html_message=html_message)

    return(emailVer)