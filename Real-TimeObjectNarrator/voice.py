from pygame import mixer
import time
from gtts import gTTS

tts = gTTS("hello my name is tvlps")  
tts.save("hello.mp3")  

mixer.init()
mixer.music.load("hello.mp3")
mixer.music.play()
while mixer.music.get_busy():
    time.sleep(1)
