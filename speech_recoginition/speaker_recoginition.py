import pveagle
import os
import pvfalcon
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from pydub import AudioSegment

access_key = os.environ.get("API_KEY")
print(access_key)
audio_directory = "audio"

def create_audio(count, bitrate="192k"):

    freq = 44100
    
    duration = 10
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)
    sd.wait()
    

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)
    write(f"{audio_directory}\\user_{count}.wav", freq, recording)

    wv.write(f"{audio_directory}\\user_{count}.wav", recording, freq, sampwidth=2)
def diaritize(path):
    access_key = os.environ.get("API_KEY")
    falcon = pvfalcon.create(access_key=access_key)

    segments = falcon.process_file(path)
    for segment in segments:
        print(
            "{speaker_tag=%d start_sec=%.2f end_sec=%.2f}"
            % (segment.speaker_tag, segment.start_sec, segment.end_sec)
        )

create_audio(1)
#diaritize(f"{audio_directory}\\user_1.wav")

