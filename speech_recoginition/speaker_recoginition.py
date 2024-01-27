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
    name =f"user_{count}.wav"
    if count<0:
        name = "transcript.wav"

    write(f"{audio_directory}\\{name}", freq, recording)

    wv.write(f"{audio_directory}\\{name}", recording, freq, sampwidth=2)

def diaritize(path):
    falcon = pvfalcon.create(access_key=access_key)

    segments = falcon.process_file(path)
    for segment in segments:
        print(
            "{speaker_tag=%d start_sec=%.2f end_sec=%.2f}"
            % (segment.speaker_tag, segment.start_sec, segment.end_sec)
        )
    return segments
def trim_audio(input_path, count, start_ms, end_ms):
    audio = AudioSegment.from_wav(input_path)
    trimmed_audio = audio[start_ms:end_ms]
    trimmed_audio.export(f"{audio_directory}\\trim_{count}.wav", format="wav")


create_audio(-1)
print("someone else talk")
#create_audio(2)
#trim_audio(f"{audio_directory}\\user_1.wav",1,0, 2500)
segments=diaritize(f"{audio_directory}\\transcript.wav")
speakers= set()
for segment in segments:
    if segment.speaker_tag not in speakers:
        speakers.add(segment.speaker_tag)
        trim_audio(f"{audio_directory}\\transcript.wav",segment.speaker_tag, segment.start_sec,segment.end_sec)

