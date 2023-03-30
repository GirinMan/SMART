import requests
import json
import base64

# Set the API endpoint URL
url = "WHISPER_API_SERVER_URL/transcribe"

def get_transcription(wav_data:bytes):
    file_base64 = base64.b64encode(wav_data)
    file_base64_str = file_base64.decode()

    # Create a dictionary containing the file data
    file_data = json.dumps({"file": file_base64_str})

    # Send a POST request to the API with the file data
    response = requests.post(url, data=file_data)

    # Check if the request was successful (status code 200)
    if response.ok:
        return response.json()['text']
    else:
        # If the request failed, print the error message returned by the API
        error_msg = response.json()["detail"]
        print(f"API error: {error_msg}")
        return None

if __name__ == "__main__":

    # Set the path to your input WAV file
    file_path = "../test.wav"

    # Read the input WAV file as bytes
    with open(file_path, "rb") as file:
        file_bytes = file.read()

    response = get_transcription(file_bytes)
    print(response)
