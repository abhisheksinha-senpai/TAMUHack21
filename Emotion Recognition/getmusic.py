from matplotlib import pyplot as plt
import face_recognition
from PIL import Image as img, ImageDraw
from fer import FER
from IPython.display import Image, display
import pandas as pd

def getTrackFilename(current_name):
    track = getfeeling(current_name)

    df = pd.read_csv('temp.csv')
    print("printing dataframe before filter")
    val1 = df.loc[df['Emotion_tmp'] == int(track)]
    val1 = val1.sample(frac =1)
    return val1[['Nro','Album_name', 'location', 'Emotion']]



def getfeeling(current_name):
    image = face_recognition.load_image_file(current_name)
    face_locations = face_recognition.face_locations(image)
    current_name_c=current_name.split('.')
    current_name_tmp=current_name_c[0]+'1.'+current_name_c[1]
    print(current_name_tmp)
    with img.open(current_name) as im:
      im=im.convert('RGB')
      draw = ImageDraw.Draw(im)
      #im.show()
      for location in face_locations:
          top, right, bottom, left = location
          draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=1)
      #del(draw)
          crop_rectangle = (left, top, right, bottom)
          cropped_im = im.crop(crop_rectangle)

          display(cropped_im)

          cropped_im.save(current_name_tmp)
        #display(im)
    test=plt.imread(current_name_tmp)
    #plt.imshow(test)

    temp=FER(mtcnn=True)
    test=plt.imread(current_name_tmp)
    captured=temp.detect_emotions(test)
    captured=captured[0]
    print(captured)
    emotions = captured['emotions']
    print(emotions,type(emotions))
    maxi=0
    ind=0
    for i,(key,value) in enumerate(emotions.items()):
        m=float(value)
        if m>maxi:
            ind=i
            maxi=m

    return str(ind)
