"""
This is a simple flask app where you can send an email from a
gmail account. To do this:

1) Setup a team gmail account with a username/password
2) Follow these instructions to allow gmail to be OK with these emails
   https://www.dev2qa.com/how-do-i-enable-less-secure-apps-on-gmail/
3) Fill in the username and password in this script
4) Run the flask app, and access /send-mail

"""

from flask_mail import Message
from server import mail, APP

def send_mail(resetCode, email):
    with APP.app_context():
        try:
            msg = Message("slackr passwordreset",
                sender="nomoreprojectpls@gmail.com",
                recipients=[email])
            msg.body = resetCode
            mail.send(msg)
            return "SUCCESS"
        except Exception:
            return "ERROR"
