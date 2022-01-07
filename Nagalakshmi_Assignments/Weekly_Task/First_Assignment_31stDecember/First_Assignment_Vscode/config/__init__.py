from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import boto3

app = Flask(__name__, static_url_path="")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_URL_PATTERN")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
client = boto3.client('s3',
                      region_name='ap-south-1',
                      # creates a new folder inside it
                      # endpoint_url='https://python-bucket77.s3.ap-south-1.amazonaws.com',
                      aws_access_key_id=os.getenv('ACCESS_KEY'),
                      aws_secret_access_key=os.getenv('SECRET_KEY')
                      )
