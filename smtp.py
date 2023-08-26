from django.core.mail import send_mail
from random import randint
from django.conf import settings
from account.models import CustomUser
import smtplib



def send_otp_via_email(email):
    """Generate OTP and send to user gmail"""

    otp = randint(100000, 999999)
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(
            user='belovedvince@gmail.com',
            password='gbblpjyscccxpyvr'
            )
        connection.sendmail(
            from_addr='belovedvince@gmail.com',
            to_addrs='vinceoludare@gmail.com',
            msg=f"Subject: OTP verification \n\n\n Your otp code is {otp}"
        )
