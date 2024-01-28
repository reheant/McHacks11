import os
import pvfalcon
import pvleopard
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from pydub import AudioSegment
import re


audio_directory = "audio"
summ = 0
ended = False
def create_audio(name="transcript.wav", bitrate="192k"):
    freq = 44100
    duration = 10
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    sd.wait()
    
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    file_path = os.path.join(audio_directory, name)
    write(file_path, freq, recording)
    wv.write(file_path, recording, freq, sampwidth=2)

def diaritize(path):
    access_key = os.environ.get("API_KEY")
    falcon = pvfalcon.create(access_key=access_key)
    segments = falcon.process_file(path)
    return segments

def trim_audio(input_path, count, start_ms, end_ms):
    audio = AudioSegment.from_wav(input_path)
    trimmed_audio = audio[start_ms*1000:end_ms*1000]
    trimmed_file_path = os.path.join(audio_directory, f"trim_{count}.wav")
    trimmed_audio.export(trimmed_file_path, format="wav")

def create_trims():
    transcript_path = os.path.join(audio_directory, "transcript.wav")
    segments = diaritize(transcript_path)
    speakers = set()
    for segment in segments:
        if segment.speaker_tag not in speakers:
            speakers.add(segment.speaker_tag)
            trim_audio(transcript_path, str(segment.speaker_tag), int(segment.start_sec * 1000), int(segment.end_sec * 1000))

def merge(file1, file2, file3 = "merged.wav") -> str:
    audio1 = AudioSegment.from_wav(file1)
    audio2 = AudioSegment.from_wav(file2)
    merged_audio = audio1 + audio2
    merged_file_path = os.path.join(audio_directory, file3)
    merged_audio.export(merged_file_path, format="wav")
    return merged_file_path

def compare(input) -> bool:
    segments = diaritize(input)
    tags = []
    for segment in segments:
        if segment.speaker_tag not in tags:
            tags.append(segment.speaker_tag)
    if len(tags)>2:
        return False
    return True

def match() -> dict:
    matches = {}
    all_files = os.listdir(audio_directory)
    trimmed_files = [file for file in all_files if file.startswith("trim")]
    user_files = [file for file in all_files if not file.startswith("trim") and file != "transcript.wav"and not file=="sample.wav" and not file=="merged.wav" and not file[0].isdigit()]
    for trimmed_file in trimmed_files:
        for user_file in user_files:
            user_file_path = os.path.join(audio_directory, user_file)
            trimmed_file_path = os.path.join(audio_directory, trimmed_file)
            merged = merge(user_file_path, trimmed_file_path)
            merged_file_path= os.path.join(audio_directory, "merged.wav")
            sample_file_path= os.path.join(audio_directory, "sample.wav")
            merged = merge(merged_file_path,sample_file_path)  
            match = re.search(r'\d+', trimmed_file)
            if match and compare(merged):
                matches[match.group()] = user_file.replace(".wav", "")
                found=True
                break
        if not found:
            matches[match.group()] = "UNKNOWN"
    return matches

def timestamps():
    leopard = pvleopard.create(access_key=access_key)
    transcript_file_path= os.path.join(audio_directory, "transcript.wav")
    transcript, words = leopard.process_file(transcript_file_path)
    leopard.delete()
    return words
def transcript():
    times = timestamps()
    transcript_file_path= os.path.join(audio_directory, "transcript.wav")
    seperated=diaritize(transcript_file_path)
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

def record():
    summ=0
    transcript_path = os.path.join(audio_directory, "transcript.wav")
    while not ended:
        file_path = os.path.join(audio_directory, f"{summ}_transcript.wav")
        if summ>0:
            create_audio(f"{summ}_transcript.wav")
            merge(transcript_path,file_path, "transcript.wav")
        else:
            create_audio("transcript.wav")
        summ+=10
    

if __name__ =="__main__":

    access_key = os.environ.get("API_KEY")
    #create_audio("Richard.wav")
    #print("swap")
    #create_audio("Andrew.wav")
    #print("swap")
    #create_audio()
    #create_trims()
    ##print(match())
    #print(transcript())
    record()

    








