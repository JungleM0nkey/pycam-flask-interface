#!/usr/bin/python3.8
from flask import Flask, render_template
from picamera import PiCamera
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os
import sys


#flask config
app = Flask(__name__)
camera = PiCamera()
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


import models #this is needed to be here able to import $db into models.py
from models import Image


#functions
def capture():
    #camera.start_preview()
    #sleep(2)
    original_date = str(time.asctime())
    date = original_date.replace(' ', '_').replace(':','_')
    filename = f'capture_{date}.jpg'
    filepath = f'/home/pi/pycam/static/images/captures/{filename}'
    camera.capture(filepath)
    return (filename, filepath, original_date)
    #camera.close()
    #camera.stop_preview()

def updatedb(new_capture, new_capture_date):
    new_image = Image(filename=new_capture, date=new_capture_date)
    db.session.add(new_image)
    db.session.commit()

def getcaptures(num):
    #returns the last x amount of Images, sorted by Descending Image ID
    capture_objects = Image.query.order_by(Image.id.desc()).limit(num).all() 
    #reverse list for web order
    capture_objects.reverse()
    return capture_objects

#routes
@app.route('/')
def index():
    #get new capture and new capture info
    new_capture, new_capture_path, new_capture_date = capture()
    #update db with new capture info
    updatedb(new_capture, new_capture_date) 
    capture_objects = getcaptures(7)
    return render_template('index.html', new_capture=new_capture, new_capture_date=new_capture_date, capture_objects=capture_objects)

if __name__ == '__main__':
    app.run(host='0.0.0.0')