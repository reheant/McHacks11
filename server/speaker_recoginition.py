import os
import pvfalcon
import pvleopard
import pveagle
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from pydub import AudioSegment
import re
import wave
import numpy as np
import librosa
import soundfile as sf


audio_directory = "audio"

def create_audio(name="transcript.wav", bitrate="192k"):

    freq = 44100
    
    duration = 10
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=1)
    sd.wait()
    

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    write(f"{audio_directory}\\{name}", freq, recording)

    wv.write(f"{audio_directory}\\{name}", recording, freq, sampwidth=2)



def diaritize(path):
    access_key = os.environ.get("API_KEY")
    falcon = pvfalcon.create(access_key=access_key)

    segments = falcon.process_file(path)
    return segments
def trim_audio(input_path, count, start_ms, end_ms):
    audio = AudioSegment.from_wav(input_path)
    trimmed_audio = audio[start_ms*1000:end_ms*1000]
    trimmed_audio.export(f"{audio_directory}\\trim_{count}.wav", format="wav")

def create_trims():
    segments=diaritize(f"{audio_directory}\\transcript.wav")
    speakers= set()
    for segment in segments:
        if segment.speaker_tag not in speakers:
            speakers.add(segment.speaker_tag)
            trim_audio(f"{audio_directory}\\transcript.wav",segment.speaker_tag, segment.start_sec,segment.end_sec)


def merge (file1, file2)->str:

    audio1 = AudioSegment.from_wav(file1)
    audio2 = AudioSegment.from_wav(file2)

    merged_audio = audio1 + audio2

    merged_audio.export(f"{audio_directory}\\merged.wav", format="wav")
    return f"{audio_directory}\\merged.wav"


def compare(input)-> bool:
    segments = diaritize(input)
    tags = []
    for segment in segments:
        if segment.speaker_tag not in tags:
            tags.append(segment.speaker_tag)
    if len(tags)>2:
        return False
    return True

def match()-> dict:
    matches = {}
    all_files = os.listdir("audio")
    trimmed_files = [file for file in all_files if file.startswith("trim")]
    user_files = [file for file in all_files if not file.startswith("trim") and not file=="transcript.wav"and not file=="sample.wav" and not file=="merged.wav"]
    found=False
    for trimmed_file in trimmed_files:
        for user_file in user_files:
            merged = merge(f"{audio_directory}\\{user_file}", f"{audio_directory}\\{trimmed_file}")
            merged = merge(f"{audio_directory}\\merged.wav",f"{audio_directory}\\sample.wav")       
            match = re.search(r'\d+', trimmed_file)
            if compare(merged):
                matches[match.group()] = user_file.replace(".wav", "")
                found=True
                break
        if not found:
            matches[match.group()] = "UNKNOWN"
    return matches

def timestamps():
    leopard = pvleopard.create(access_key=access_key)
    transcript, words = leopard.process_file(f"{audio_directory}\\transcript.wav")
    leopard.delete()
    return words
def transcript():
    times = timestamps()
    seperated=diaritize("audio\\transcript.wav")
    count=0
    matches= match()
    previous = matches[str(seperated[count].speaker_tag)]
    output = f"{previous}: "
    endtime= float(seperated[0].end_sec)
    for time in times:
        if time.start_sec>endtime:
            count+=1
            output+="\n"
            previous = matches[str(seperated[count].speaker_tag)]
            output+=f"{previous}: "
            endtime=float(seperated[count].end_sec)
            
        else:
            output+=f"{time.word} "
    return output

def full_transcript():
    create_trims()
    return full_transcript()

if __name__ =="__main__":

    access_key = os.environ.get("API_KEY")
    create_audio("Richard.wav")
    print("swap")
    create_audio("Andrew.wav")
    print("swap")
    create_audio()
    create_trims()
    #print(match())
    print(transcript())

    








