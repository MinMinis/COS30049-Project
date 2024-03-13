
from random import choice , randint
from django.conf import settings
from .models import *
from django.core.mail import EmailMessage


#Used to create an OTP code consisting of 5 digits
def generate_OTP():
    otp_code = ""
    for i in range(5) : 
        otp_code  += choice("123456789")
    return otp_code

# Used to send otp to mail to verify that account is valid
def send_otp_via_email(email) : 
    subject = "Your account verification email : "
    otp_code = generate_OTP()
    user = User.objects.get(email=email)
   # Get or create data based on a condition -> return 2 elements(otp_instance(OneTimePassword object) and created (boolean -> if created and true if not ))
    otp_instance, created = OneTimePassword.objects.get_or_create(
        user=user, defaults={'code': otp_code, 'expiration_time': timezone.now() + timezone.timedelta(minutes=1)}
    )
    # If the object already exists, update its OTP code and expiration time
    if not created:
        otp_instance.code = otp_code
        otp_instance.expiration_time = timezone.now() + timezone.timedelta(minutes=1)
        otp_instance.save()

    user.otp = otp_code
    user.save()
    #Calculate expiration time (1 minute after current time)
    expiration_time = timezone.now() + timezone.timedelta(minutes=1)
    current_site = "Digicode"
    email_body = f"Dear {user.first_name},\n\nThank you for signing up on {current_site}. We appreciate your registration.\n\n"\
                f"To verify your email and complete the registration process, please use the following one-time passcode: {otp_code}.\n\n"\
                f"If you have any questions or need assistance, feel free to contact our support team.\n\n"\
                f"Best regards,\n{current_site}"
    from_email = settings.EMAIL_HOST
    d_mail = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_mail.send(fail_silently=True)


def send_otp_via_email_for_reset(email):
    subject = "Your account verification email: "
    otp_code = generate_OTP()
    user = User.objects.get(email=email)

    otp_instance, created = SaveEmailModel.objects.update_or_create(
        email=email,
        defaults={'code': otp_code, 'expiration_time': timezone.now() + timezone.timedelta(minutes=1)}
    )

    expiration_time = timezone.now() + timezone.timedelta(minutes=1)

    current_site = "Digicode"
    email_body = f"Hi {user.first_name}, thank you for signing up on {current_site}. Please verify your email with the one-time passcode: {otp_code}."
    from_email = settings.EMAIL_HOST
    d_mail = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_mail.send(fail_silently=True)


