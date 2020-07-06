#!/usr/bin/python3.8
from flask import Flask, render_template, url_for, redirect, session, request, Response
from picamera import PiCamera
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from forms import SettingsForm
from pathlib import Path
import os
import sys


#flask config
app = Flask(__name__)
app.config.from_object(Config)
basedir = Config.APP_BASEDIR #main directory of the app
db = SQLAlchemy(app)
migrate = Migrate(app, db)


import models #this is needed to be here able to import $db into models.py
from models import Image, Settings

#functions
def capture():
    original_date = str(time.asctime())
    date = original_date.replace(' ', '_').replace(':','_')
    filename = f'capture_{date}.jpg'
    filepath = Path(f'{basedir}/static/images/captures/{filename}')
    with PiCamera() as camera: 
        #get settings for camera and apply them
        res_x, res_y, rotation, effect = getsettings()
        applycamsettings(camera, res_x, res_y, rotation, effect)
        camera.capture(str(filepath))
    return (filename, filepath, original_date)
    #camera.stop_preview()

def updatedb(new_capture, new_capture_date):
    new_image = Image(filename=new_capture, date=new_capture_date)
    db.session.add(new_image)
    db.session.commit()

def getcaptures(day):
    #capture_objects = Image.query.order_by(Image.id.desc()).limit(num).all() #returns the last x amount of Images, sorted by Descending Image ID
    capture_objects = Image.query.filter(Image.date.contains(day)).order_by(Image.id.desc()).all()
    #reverse list for web order
    capture_objects.reverse()
    return capture_objects

def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

def getdays():
    capture_objects = Image.query.all() 
    capture_dates = [ x.date for x in  capture_objects ]
    capture_days = [ x.split(' ')[0:4] for x in capture_dates ]
    capture_days = [ ' '.join(x) for x in capture_days ]
    capture_days = [ x[0:10] for x in capture_days ]
    capture_days = unique(capture_days)
    capture_days.reverse()
    return capture_days

def getsettings():
    settings = Settings.query.first()
    #check if no settings are set 
    if not settings:
        print('Settings are missing, setting defaults')
        default_settings = Settings(res_x=1920,res_y=1080,rotation=180,effect='none')
        db.session.add(default_settings)
        db.session.commit()
    settings = Settings.query.first()
    return (settings.res_x, settings.res_y, settings.rotation, settings.effect)

#applies new camera settings
def applycamsettings(camera, res_x, res_y, rotation, effect):
    if camera.previewing:
        print('Camera previewing. Stopping camera.')
        camera.stop_preview()
        #camera.close()
        #print(camera.previewing)
    print(f'Applying settings to camera. Resolution: {res_x}x{res_y}, Rotation: {rotation}, Effect: {effect}')
    camera.resolution = (res_x, res_y)
    print('Resolution set')
    camera.rotation = rotation
    print('Rotation set')
    camera.image_effect = effect
    print('Effect set')

def gen():
    with PiCamera() as camera:
        #get settings for camera and apply them
        res_x, res_y, rotation, effect = getsettings()
        applycamsettings(camera, res_x, res_y, rotation, effect)
        camera.start_preview()
        filepath = Path(f'{basedir}/static/images/stream/')
        jpg_file = filepath / "image1.jpg"
        while camera.previewing:
            #create images
            for i, filename in enumerate(camera.capture_continuous(str(jpg_file))):
                #send image
                #frame = open('/home/pi/pycam/static/images/stream/image1.jpg', 'rb').read()
                frame = open(jpg_file, 'rb').read()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                if i >= 0:
                    break

#routes
@app.route('/', methods=['GET'])
def root():
    #get new capture and new capture info
    new_capture, new_capture_path, new_capture_date = capture()
    #update db with new capture info
    updatedb(new_capture, new_capture_date) 
    capture_days = getdays()
    latest_day = capture_days[0]
    day=latest_day.replace(' ', '_')
    #save all the data to a session
    session['data'] = (new_capture, new_capture_date, capture_days)
    next_page = url_for('index', day=day)
    return redirect(next_page)

@app.route('/index/<day>', methods=['GET','POST'])
def index(day):
    form = SettingsForm()
    new_capture, new_capture_date, capture_days = session['data']
    res_x, res_y, rotation, effect = getsettings()
    #this is the only way to set default values for select form inputs
    form.res_x.default = res_x
    form.res_y.default = res_y
    form.rotation.default = rotation
    form.effect.default = effect
    form.process()
    capture_objects = getcaptures(day.replace('_', ' '))
    return render_template('index.html',form=form, 
                                        new_capture=new_capture, 
                                        new_capture_date=new_capture_date, 
                                        capture_days=capture_days, 
                                        capture_objects=capture_objects,
                                        res_x = res_x,
                                        res_y = res_y,
                                        rotation = rotation,
                                        effect = effect,
                                        )        

@app.route('/savesettings', methods=['POST'])
def savesettings():
    #grab values from frontend
    res_x = int(request.form['res_x'])
    res_y = int(request.form['res_y'])
    rotation = int(request.form['rotation'])
    effect = str(request.form['effect'])
    #apply and save
    try:
        existing_settings = Settings.query.first()
        existing_settings.res_x = res_x
        existing_settings.res_y = res_y
        existing_settings.rotation = rotation
        existing_settings.effect = effect
        #applycamsettings(res_x, res_y, rotation, effect) #apply the settings
        db.session.commit() #save the settings
        return u'Settings saved', 200
    except Exception as e:
        print(e)
        return f'Settings not saved: {e}', 500

@app.route('/stream', methods=['GET','POST'])
def stream():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame' )
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')