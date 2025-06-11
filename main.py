import requests
from fastapi import FastAPI

app = FastAPI()

WAZZUP_TOKEN = "4e68fe2f438140b0ba531c114509b1e9"  # замени, если потребуется


@app.get("/")
def get_channel_id():
    url = "https://api.wazzup24.com/v3/channels"
    headers = {
        "Authorization": f"Bearer {WAZZUP_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        channels = response.json()
        result = []
        for channel in channels:
            result.append({
                "name": channel.get("name"),
                "id": channel.get("id"),
                "channelType": channel.get("channelType")
            })
        return result
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }
