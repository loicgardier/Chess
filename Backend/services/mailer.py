from smtplib import SMTP
from dotenv import load_dotenv
import os

from email.message import EmailMessage

load_dotenv()


class Mailer:

    def send_mail(self,subject:str, dest: str, body: str):
        msg = EmailMessage()
        msg['To']=[dest]
        msg['Subject']=subject
        msg['From']=os.environ['MAIL_ADMIN']
        msg.add_alternative(body, subtype="html")
        with SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as smtp:
            smtp.send_message(msg)


