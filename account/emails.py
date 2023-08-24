from random import randint
from account.models import CustomUser
import smtplib
from smtplib import SMTPConnectError, SMTPAuthenticationError, SMTPDataError, SMTPException
from Investflow.settings import EMAIL_HOST_USER
from Investflow.settings import EMAIL_HOST_PASSWORD
from Investflow.settings import EMAIL_HOST
from account.models import CustomUser
from django.http import JsonResponse


def send_otp_via_email(email):
    """Generate OTP and send to user gmail"""

    generated_otp = randint(100000, 999999)
    try:
        with smtplib.SMTP(EMAIL_HOST) as connection:
            connection.starttls()
            connection.login(
                user=EMAIL_HOST_USER,
                password=EMAIL_HOST_PASSWORD
                )
            connection.sendmail(
                from_addr=EMAIL_HOST_USER,
                to_addrs=email,
                msg=f"Subject: OTP verification \n\n\n Your otp code is: {generated_otp}"
            )
            user_obj = CustomUser.objects.get(email=email)
            user_obj.otp = generated_otp
            user_obj.save()

    except (SMTPConnectError, SMTPAuthenticationError, SMTPDataError, SMTPException, Exception) as e:
        return JsonResponse(
            {
                'status': 400,
                "message": "Something went wrong"
            }
        )
        
