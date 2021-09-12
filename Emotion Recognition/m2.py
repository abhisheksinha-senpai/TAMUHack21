import pandas as pd
import math
data=pd.read_csv('set1_tracklist.csv')
data = data.head(180)

def emotion_func(x):
    if x == 'Anger':
        x='0'
    elif x == 'Fear':
        x='2'
    elif x == 'Happy':
        x='3'
    elif x == 'Sad':
        x='4'
    elif x == 'Surprise':
        x='5'
    elif x ==  'Tender':
        x='6'
    else:
        x=x
    return x

def location_from_nro(x):
    no_of_digits = int(math.log(int(x),10))
    diff = 2- no_of_digits
    return "Set1/" + str("0"*diff) + str(x) +".mp3"

data['Emotion_tmp']=data['Emotion'].apply(emotion_func)
data['location']=data['Nro'].apply(location_from_nro)
data.to_csv('temp.csv')
