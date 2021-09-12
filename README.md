# TAMUHack21
Tamu HACK 2021 hand gesture detection
Idea :
The idea has 2 steps:
Mood Detection and Music Selection
Play music to suit the user’s mood.
Music Navigation using Hand Gestures
Change played song or volume level by simple hand movements.


###
Detail(Code in Emotion Recognition)
1. First, capture the image of the face of the user using the Webapp interface. 
2. Next, run face recognition algorithm to identify face in the Image.
3. Crop Image to include only the face.
4. Use the captured image to obtain Mood of the person
5. We will try to classify the person’s Possible Moods {Anger, Fear, Happy, Sad, Surprise,Normal} using FER(Facial Emotional Recognition Model).
6. Using this we will suggest a list of Songs based on the Mood of the person.

###
Details(Code in Gestures.py)
1.First, detect the hand of the user using MediaPipe. 
2.Next, define mathematical constructs to decipher different types of motions/gestures, with a threshold value, so as to not detect any command at unintentional movements.
3.Finally, associate each movement to a media player action and pass these action commands to the web app for execution.

Languages: Python, HTML, CSS, Javascript
Framework: Flask

###
DataSet:
We have used Music and emotion stimulus sets consisting of film soundtracks dataset for playing Music
Dataset URL: https://osf.io/t5pk3/

###
Progress
1. We have created the web app to capture and save the image of the user.
2. Then mood of the user is predicted and a song is recommended based on the facial expressions
3. Gestures next come in, to help navigate and control the music independent of song recommendation engine. 
4. It involves two gestures as of now - horizontal swipe (prev song or next song) and vertical swipe (Volume control).

###
Future
1. The first direction is to complete the integration of both the components.
2. Second is to move on from mood capturing from image to do the same using videos.
3. Redirect user to songs hosted on a public website like YouTube or Spotify rather than have them saved on the user system.
4. Allow user to give feed back on the song selection and incorporate this feature in future recommendations. 
5. Expand spectrum of hand gesture recognition.



How to execute:
1. Install face-recognition, FER, MediaPipe and other basic libraries of python
2. To run the webapp for Songs Recommendation using Mood python3 app.py
3. Visit localhost:5000/capture
4. Take an image which will then redirect to localhost:5000/ and will recommend songs.
5. Also Run python3 gestures.py which will open a Python GUI which will show you the left/right and up/down gesture which can be used for songs control.
