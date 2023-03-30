import requests
import json

# Set the API endpoint URL
url = "SUMMARY_API_SERVER_URL/summarize"

def get_summarization(text:str):

    # Create a dictionary containing the file data
    file_data = json.dumps({"text": text})

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

    text = "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."

    response = get_summarization(text)
    print(response)
