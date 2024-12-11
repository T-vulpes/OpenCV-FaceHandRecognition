from pygame import mixer
import time
from gtts import gTTS

# gTTS nesnesi oluşturma
tts = gTTS("hello my name is tvlps")  # Burada bir gTTS nesnesi oluşturuluyor
tts.save("hello.mp3")  # gTTS nesnesini kaydediyoruz

# Pygame ile ses çalma
mixer.init()
mixer.music.load("hello.mp3")
mixer.music.play()
while mixer.music.get_busy():
    time.sleep(1)
