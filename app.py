from flask import Flask,redirect,url_for,request
from flask.templating import render_template
import cv2
import numpy as np
import sounddevice
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.playback import play
#import pandas as pd
import os
from csv import reader



app=Flask(__name__)

if __name__=="__main__":
    app.run(debug=True)



@app.route('/')
def first():
    return render_template('name_entry.html')

@app.route('/entry',methods=['POST','GET'])
def imgcapture():
    if request.method=='POST':
        camera=cv2.VideoCapture(0)
        success,frame=camera.read()
        raw = request.values.get("fname")  
        first_name = request.values.get("fname")  
        if not os.path.exists(first_name):
            os.makedirs(first_name)
        first_name=first_name+'/'+first_name+'.png'
        cv2.imwrite(first_name,frame)
        f = open("folder_name.txt", "w")
        f.write(raw)
        f.close()
        
        j='Test your voice Now!!!'
    next_page='questions.html'
    return render_template(next_page, question=j)


@app.route('/next',methods=['POST','GET'])
def audiocapture():
    if request.method=='POST':
        with open('index.txt','r') as f:
            data = f.readlines()
            str_read = ''.join(data)
            value_int=int(str_read)
            data = value_int + 1
            string_value=str(data)
            f2 = open("index.txt", "w")
            f2.write(string_value)
            f2.close()
            #transciption=pd.read_csv("transcript.csv")
            with open('transcript.csv', 'r', encoding="utf8") as file:
                #my_reader = csv.reader(file, delimiter=',')
                my_reader = reader(file)
                #my_reader=csv.read_csv("trancript.csv")
                k=0
                for row in my_reader:
                    k=k+1
                    if k==data:
                        row_data = str(row)

    fps=44100
    duration= 6
    recording= sounddevice.rec(int(duration*fps), samplerate=fps, channels=2)
    sounddevice.wait()
    #save the audio
    with open('folder_name.txt','r') as f:
        folder_n = f.readlines()
        folder_n = ''.join(folder_n)
        folder_n= str(folder_n)
    audio_file_location=  folder_n+ '/' + str(data) + '.wav'
    write(audio_file_location, fps, recording)            
    next_page='questions.html'

    return render_template(next_page, question=row_data)


@app.route('/restart',methods=['POST','GET'])
def restart():

    f2 = open("index.txt", "w")
    f2.write('0')
    f2.close()
    return render_template("name_entry.html")