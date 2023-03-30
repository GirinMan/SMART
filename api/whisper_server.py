import torch
import whisper
from fastapi import FastAPI
import base64
from pydantic import BaseModel, Field
from typing import Dict
from tempfile import NamedTemporaryFile

temp_file = NamedTemporaryFile().name

model = "large"
if model != "large":
    model = model + ".en"
audio_model = whisper.load_model(model)

def transcribe(wav_data):
    with open(temp_file, 'w+b') as f:
        f.write(wav_data)
    result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available())
    return result['text'].strip()

app = FastAPI(title='whisper',
              description='whisper-medium.en',
              version="1.0")

class AudioData(BaseModel):
    file: str

class textResponse(BaseModel):
    text: str = Field(None, description="Transcribed texts")

@app.get("/")
def home():
    return "Refer to '/docs' for API documentation"

number = 0

@app.post("/transcribe", response_model=textResponse)
async def get_transcription(audio_data: AudioData):
    """Prediction
    :param req_body:
    :return:
    """
    global number
    file_base64_str = audio_data.file
    file_bytes = base64.b64decode(file_base64_str)

    filename = f"./temp/temp_server_{number}.wav"
    number += 1
    with open(filename, "wb") as f:
        f.write(file_bytes)
    
    text = audio_model.transcribe(filename, fp16=torch.cuda.is_available())['text']
    return {"text": text}

