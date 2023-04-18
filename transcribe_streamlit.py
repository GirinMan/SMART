#! python3.7

import argparse
import io
import speech_recognition as sr
import streamlit as st
import os

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform
from api.translation_api import get_translation
from api.papago_api import get_papago_detection, get_papago_trans
from api.whisper_api import get_transcription
from api.summary_api import get_summarization
from api.title_api import get_title

st.set_page_config(layout="wide")
st.title("S.M.A.R.T. DEMO")
st.markdown("## Spoken Media Automatic Reconstruction Tool")
st.markdown("""
- Real-time transcription with automatic summarization
- Made by Seongjin Lee(http://github.com/GirinMan)""")

parser = argparse.ArgumentParser()
parser.add_argument("--model", default="medium", help="Model to use",
                    choices=["tiny", "base", "small", "medium", "large"])
parser.add_argument("--non_english", action='store_true',
                    help="Don't use the english model.")
parser.add_argument("--energy_threshold", default=1000,
                    help="Energy level for mic to detect.", type=int)
parser.add_argument("--record_timeout", default=3,
                    help="How real time the recording is in seconds.", type=float)
parser.add_argument("--phrase_timeout", default=2,
                    help="How much empty space between recordings before we "
                            "consider it a new line in the transcription.", type=float)  
if 'linux' in platform:
    parser.add_argument("--default_microphone", default='pulse',
                        help="Default microphone name for SpeechRecognition. "
                            "Run this with 'list' to view available Microphones.", type=str)
parser.add_argument("--translator", default='custom',
                    help="Default translator for english to korean translation. Use papago or custom", type=str)
args = parser.parse_args()

# The last time a recording was retreived from the queue.
phrase_time = None
# Current raw audio bytes.
last_sample = bytes()
cached_last_sample = bytes()
# Thread safe Queue for passing data from the threaded recording callback.
data_queue = Queue()
# We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
recorder = sr.Recognizer()
recorder.energy_threshold = args.energy_threshold
# Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
recorder.dynamic_energy_threshold = False

# Important for linux users. 
# Prevents permanent application hang and crash by using the wrong Microphone
if 'linux' in platform:
    mic_name = args.default_microphone
    if not mic_name or mic_name == 'list':
        print("Available microphone devices are: ")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone with name \"{name}\" found")   
        exit()
    else:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if mic_name in name:
                print(f"Microphone with name \"{name}\" found")   
                source = sr.Microphone(sample_rate=16000, device_index=index)
                break
else:
    source = sr.Microphone(sample_rate=16000)

record_timeout = args.record_timeout
phrase_timeout = args.phrase_timeout

if args.translator == "custom":
    translate = get_translation
elif args.translator == "papago":
    translate = lambda x: get_papago_trans(x)['translatedText']
else:
    translate = lambda x: x

temp_file = NamedTemporaryFile().name
transcription_file = "./trans.txt"
transcription = []
summary = []
title = []
target_lang = 'ko'
block_size = 600
sentence_size = 100

with source:
    recorder.adjust_for_ambient_noise(source)

def record_callback(_, audio:sr.AudioData) -> None:
    """
    Threaded callback function to recieve audio data when recordings finish.
    audio: An AudioData containing the recorded bytes.
    """
    # Grab the raw bytes and push it into the thread safe queue.
    data = audio.get_raw_data()
    data_queue.put(data)

# Create a background thread that will pass us raw audio bytes.
# We could do this manually but SpeechRecognizer provides a nice helper.
recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

def show_contents(col1, col2):
    for i, (line, summ, _title) in enumerate(zip(transcription, summary, title)):
        st.markdown("---------")
        split_title = _title.split("###")
        if len(split_title) > 1:
            st.markdown(f"#### Section {i} | {split_title[1]}")
            st.markdown(f'##### {split_title[0]}')
        else:
            st.markdown(f"#### Section {i} | {split_title[0]}")
        col1, col2 =st.columns([1, 1])
        col1.markdown('- **Transcription:** ' + line)
        col2.markdown(summ)


# Cue the user that we're ready to go.
col1, col2 = st.columns([1, 1])
col1.markdown(f"### Original transcription")
col2.markdown(f"### Summarization")

if col1.button("START", type='primary'):
    stop_button = col2.button("STOP", type='primary')
    col1, col2 = st.columns([1, 1])

    contents = st.empty()


    while True:
        with contents.container():
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    cached_last_sample = last_sample
                    last_sample = bytes()
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now

                # If we detected a pause between recordings, add a new item to our transcripion.
                # Otherwise edit the existing one.
                if phrase_complete:
                    # Use AudioData to convert the raw data to wav data.
                    audio_data = sr.AudioData(cached_last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    # Write wav data to the temporary file as bytes.
                    byte_data = wav_data.read()

                    # Read the transcription.
                    text = get_transcription(byte_data)

                    if len(transcription) > 0 :
                        transcription[-1] = transcription[-1].replace('...', '')
                        last_len = len(transcription[-1])
                        if last_len < block_size and len(text) < (block_size - last_len):
                            transcription[-1] = transcription[-1] + ' ' + text
                        else:
                            summarization = get_summarization(transcription[-1])
                            trans_summarization = translate(summarization).strip()
                            summary[-1] = '- **English:** ' + summarization + '\n- **한국어:** ' + trans_summarization
                            title[-1] = get_title(transcription[-1])
                            title[-1] += "###" + translate(title[-1])
                            transcription.append(text)
                            summary.append("")
                            title.append("")
                    else:
                        transcription.append(text)
                        summary.append("")
                        title.append("")


            elif len(summary) > 0:
                if summary[-1] == "" and len(transcription[-1]) > 100:
                    summarization = get_summarization(transcription[-1])
                    trans_summarization = translate(summarization).strip()
                    summary[-1] = '- **English:** ' + summarization + '\n- **한국어:** ' + trans_summarization
                    title[-1] = get_title(transcription[-1])
                    title[-1] += "###" + translate(title[-1])

            show_contents(col1, col2)

            with open("cache/transcription.txt", "w") as file:
                file.writelines([_txt + '\n' for _txt in transcription] + ["<end>"])
            with open("cache/summary.txt", "w") as file:
                tmp_summary = []
                for summ in summary:
                    tmp_summary.append(summ.replace('\n', ' '))
                file.writelines([_txt + '\n' for _txt in tmp_summary] + ["<end>"])
            with open("cache/title.txt", "w") as file:
                file.writelines([_txt + '\n' for _txt in title] + ["<end>"])

            if stop_button:
                break
        # Infinite loops are bad for processors, must sleep.
        sleep(0.1)

    show_contents(col1, col2)
try:
    os.makedirs("./cache", exist_ok=True)
    with open("cache/transcription.txt", "r") as file:
        transcription = file.readlines()
    with open("cache/summary.txt", "r") as file:
        summary = file.readlines()
        summary = [summ.replace("- **한", "\n- **한") for summ in summary]
    with open("cache/title.txt", "r") as file:
        title = file.readlines()

    last_index = -1
    for i, txt in enumerate(transcription):
        if "<end>" in txt:
            last_index = i
            break

    transcription = transcription[:last_index]
    summary = summary[:last_index]
    title = title[:last_index]
except:
    transcription = ["Empty document"]
    summary = ["- **English:** \n - **한국어:**"]
    title = ["Sample Title###여기에 제목 표시"]
show_contents(col1, col2)
