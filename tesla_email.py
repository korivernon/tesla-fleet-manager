import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import teslapy
from vehicle_access import *
import config

# subject = "TEST: An email with Tesla Fleet Information"
# sender_email = "kori.s.vernon@gmail.com"
# receiver_email = "koriv.tt7@gmail.com,sonnyarcilla@gmail.com"
password = config.password
# receiver_email = "koriv.tt7@gmail.com,sonnyarcilla@gmail.com"

def send_email_with_data(contents, subject = "REQUESTED EMAIL: TESLA", sender_email = config.email, receiver_email = ["koriv.tt7@gmail.com"]):
    receiver_email = ",".join(receiver_email)
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    body = "This is an email with a Tesla Fleet Information\n"

    body += str(contents)

    print("SENDING EMAIL WITH THE FOLLOWING")
    print(body)

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
