import requests
import os
from dotenv import load_dotenv

load_dotenv()

def register():
    url = "https://api.wazzup24.com/v3/webhooks"
    headers = {
        "Authorization": f"Bearer {os.getenv('WAZZUP_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": "https://bot-watsapp-bmen.onrender.com/webhook/wazzup",
        "events": ["messages"]
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Webhook registration response:", response.status_code, response.text)
