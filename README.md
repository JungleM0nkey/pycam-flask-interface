### Flask web application for accessing the Raspberry Pi v2 Camera Module through a web interface
### Note: Requires a Raspberry Pi v2 Camera Module

When the app is accessed the camera takes a snapshot and stores it under the static/images folder.
The app also allows to show a live jpeg stream to mimic a video function.


![alt text](https://i.imgur.com/HZhJSky.png "pycam preview")

Setup:
1. pip install -r requirements.txt
2. run the command: flask run
3. Navigate to http://127.0.0.1:5000/