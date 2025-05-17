from dotenv import load_dotenv
import os
load_dotenv()
passw = os.getenv("PASSW")
import smtplib
import ssl
from email.mime.text import MIMEText

def send_otp_email(user_email, otp):
    smtp_server = "hackclub.app"
    port = 587
    sender_email = "phyotp@hackclub.app"

    message = MIMEText(f'''
                       Hey there,
                        Your OTP code is: {otp}
                        Please use this code to complete your login.
                        If you did not request this code, please ignore this email.
                        
                        PhyoID
    ''')
    message["Subject"] = "PhyoID 2FA Code"
    message["From"] = sender_email
    message["To"] = user_email

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, passw)
        server.sendmail(sender_email, user_email, message.as_string())
send_otp_email("phyo.thet.pai@sji.edu.sg", "123456")