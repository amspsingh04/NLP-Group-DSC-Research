import pytubefix 
from pytubefix import YouTube
import subprocess
import torch
import os
import ffmpeg
import pandas as pd
import re

device = torch.device('cpu') #or cuda if you have cuda

audio_mp3 = "../Dataset/mp3"
audio_wav = "../Dataset/wav"
subtitles_srt = "../Dataset/srt"
subtitles_txt = "../Dataset/txt"
os.makedirs(audio_mp3, exist_ok=True)
os.makedirs(audio_wav, exist_ok=True)
os.makedirs(subtitles_srt, exist_ok=True)
os.makedirs(subtitles_txt, exist_ok=True)

df = pd.read_csv("links.csv")

i=0
for video_url in df['links']:
    try:
        yt = YouTube(video_url)
        if yt.captions:
            caption = yt.captions['en.LUU0EuDKgKo']
            if caption:
                srt_content = caption.generate_srt_captions()
                lines = srt_content.splitlines()
                txt_content = ''
                for line in lines:
                    if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
                                txt_content += ' ' + line.strip()
                txt_content = txt_content.lstrip()
                
                # File paths
                srt_file_name = f"{subtitles_srt}/vid{i}.srt"
                txt_file_name = f"{subtitles_txt}/vid{i}.txt"
                
                # Save as .srt
                with open(srt_file_name, "w", encoding="utf-8") as f:
                    f.write(srt_content)
                print(f"Subtitles saved as SRT: {srt_file_name}")
                
                # Save as .txt
                with open(txt_file_name, "w", encoding="utf-8") as f:
                    f.write(txt_content)
                print(f"Subtitles saved as TXT: {txt_file_name}")
            else:
                caption = yt.captions['a.en']
                srt_content = caption.generate_srt_captions()
                lines = srt_content.splitlines()
                txt_content = ''
                for line in lines:
                    if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
                                txt_content += ' ' + line.strip()
                txt_content = txt_content.lstrip()
                srt_file_name = f"{subtitles_srt}/vid{i}.srt"
                txt_file_name = f"{subtitles_txt}/vid{i}.txt"
                
                # Save as .srt
                with open(srt_file_name, "w", encoding="utf-8") as f:
                    f.write(srt_content)
                print(f"Subtitles saved as SRT: {srt_file_name}")
                
                # Save as .txt
                with open(txt_file_name, "w", encoding="utf-8") as f:
                    f.write(txt_content)
                print(f"Subtitles saved as TXT: {txt_file_name}")

            adst = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
            adst.download(output_path=audio_mp3, filename=f"aud{i}.mp3")
            print(f"Audio downloaded as mp3: aud{i}.mp3")
            
            subprocess.run(['ffmpeg', '-i', os.path.join(audio_mp3, f"aud{i}.mp3"), os.path.join(audio_wav, f"aud{i}.wav"), '-y'], check=True)
            print(f"Audio {i} converted to wav")
    except Exception as e:
        print(f"Failed to download subtitles for {video_url}: {e}")
    i+=1