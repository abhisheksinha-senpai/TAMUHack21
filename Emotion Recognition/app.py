from flask import Flask, render_template
import getmusic
import json
import os
import cv2
from jinja2 import Markup
from os import path

app = Flask(__name__)
@app.route('/')
def getm():
    print('home')
    df = getmusic.getTrackFilename('temp.jpeg')
    #json_object = json.dumps(df.head(20))
    return render_template('index.html',val=df.head(df.size-1).to_dict('records'))

@app.route('/capture')
def index():
    if path.exists("temp.jpeg"):
        os.remove("temp.jpeg")
    return render_template('home.html')
app.run()
