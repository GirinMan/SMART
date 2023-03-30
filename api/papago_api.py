import os
import sys
import urllib.request
import json

client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"


def get_papago_trans(text: str, source='en', target='ko'):
    request = urllib.request.Request("https://naveropenapi.apigw.ntruss.com/nmt/v1/translation")
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)

    data = f"source={source}&target={target}&text=" + urllib.parse.quote(text)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))['message']['result']
    else:
        print("Error Code:" + rescode)
        return None

def get_papago_detection(text: str):
    request = urllib.request.Request("https://naveropenapi.apigw.ntruss.com/langs/v1/dect")
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)

    data = "query=" + urllib.parse.quote(text)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
        return None



if __name__ == '__main__':
    text = "Hello. Who are you?"
    target = 'ko'
    source = get_papago_detection(text)["langCode"]
    print(get_papago_trans(text, source=source, target=target))