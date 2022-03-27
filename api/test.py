import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "medapp322@gmail.com"  # Enter your address
receiver_email = "ardan2048@gmail.com"  # Enter receiver address
password = "Qwerty2312"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    msg["Subject"] = u'MedApp Verification code'
    part1 = MIMEText(u'Your verification code: {}'.format(code),
                     "plain", "utf-8")
    msg.attach(part1)
    server.sendmail(sender_email, receiver_email, msg)