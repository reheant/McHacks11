import os
import pvfalcon
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from pydub import AudioSegment

access_key = os.environ.get("API_KEY")
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
    falcon = pvfalcon.create(access_key=access_key)

    segments = falcon.process_file(path)
    for segment in segments:
        print(
            "{speaker_tag=%d start_sec=%.2f end_sec=%.2f}"
            % (segment.speaker_tag, segment.start_sec, segment.end_sec)
        )
def trim_audio(input_path, count, start_ms, end_ms):
    audio = AudioSegment.from_wav(transc)
    trimmed_audio = audio[start_ms:end_ms]
    trimmed_audio.export(f"{audio_directory}\\transcript_{count}.wav", format="wav")


create_audio(1)
print("someone else talk")
create_audio(2)
diaritize(f"{audio_directory}\\user_1.wav")

