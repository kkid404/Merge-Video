import configparser
import os

from flask import Flask


from dotenv import load_dotenv

load_dotenv()


QIWI = os.getenv("TOKEN")
MAIL_LOG = os.getenv("LOGIN")
MAIL_PASS = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'any secret string'
