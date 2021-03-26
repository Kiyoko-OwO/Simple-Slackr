from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message

#now the code can be imported outside successfully

APP = Flask(__name__)
CORS(APP)

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='nomoreprojectpls@gmail.com',
    MAIL_PASSWORD="lizhengfanding204"
)
mail = Mail(APP)
