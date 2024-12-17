import pytubefix 
import subprocess
import torch
import os
import ffmpeg
import pandas as pd

device = torch.device('cpu') #or cuda if you have cuda


## Creating audio dataset directories
audio_mp3 = "../Dataset/mp3"
audio_wav = "../Dataset/wav"
os.makedirs(audio_mp3, exist_ok=True)
os.makedirs(audio_wav, exist_ok=True)


## Reading the links from the csv
df = pd.read_csv("links.csv")


for i in range(len(df)):
    link = df.loc[df['id'] == i, 'links'].values[0] 
    yt = pytubefix.YouTube(link)

    adst = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    if adst:
        adst.download(output_path=audio_mp3, filename=f"aud{i}.mp3") 
        subprocess.run(['ffmpeg', '-i', os.path.join(audio_mp3, f"aud{i}.mp3"), os.path.join(audio_wav, f"aud{i}.wav"), '-y'], check=True)
        print(f"Audio {i} converted to wav")
    
    