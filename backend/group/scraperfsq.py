import requests
import json
import os
import dotenv

dotenv.load_dotenv()

def generate():

    url = "https://api.foursquare.com/v3/places/search"

    params = {
        "query": "coffee",
        "ll": "47.606,-122.349358",
        "open_now": "true",
        "sort": "DISTANCE",
        "limit": 50
    }

    headers = {
        "Accept": "application/json",
        "Authorization": os.environ.get("TOWNIE_FSQ_KEY")
    }

    response = requests.request("GET", url, params=params, headers=headers)
    response1 = json.loads(response.text)
    for i in range(len(response1['results'])):
        print(response1['results'][i]['name'])

def main():
    generate()

if __name__ == "__main__":
    main()