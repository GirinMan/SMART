import torch
import copy
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import requests
import json

tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-small-medium-title-generation")
model = AutoModelForSeq2SeqLM.from_pretrained(  "fabiochiu/t5-small-medium-title-generation",
                                                torch_dtype=torch.float16,
                                                low_cpu_mem_usage=True,
                                                device_map="auto"
                                            ).eval()

def generate(text):
    tokenized_text = tokenizer(text, return_tensors='pt').to('cuda')
    with torch.no_grad():
        try:
            generated_ids = model.generate(
                **tokenized_text,
                max_new_tokens=32, # 최대 디코딩 길이
                #num_beams=3,
            )
        except:
            generated_ids = [tokenizer.eos_token_id]
            torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return generated_text

app = FastAPI(title='title_generation',
              description='fabiochiu/t5-small-medium-title-generation',
              version="1.0")


class textInput(BaseModel):
    """Input model for prediction
    """
    text: str = Field(None, description='Prompt', example="여기에 입력")    

class textResponse(BaseModel):
    text: str = Field(None, description="generated texts")

@app.get("/")
def home():
    return "Refer to '/docs' for API documentation"

@app.post("/title", description="Generation", response_model=textResponse)
def get_generation(req_body: textInput):
    """Prediction
    :param req_body:
    :return:
    """
    torch.cuda.empty_cache()
    result = generate(req_body.text)
    return {"text":result}
