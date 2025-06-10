import requests
import os
from dotenv import load_dotenv

load_dotenv()

def register():
    print("TOKEN:", os.getenv("WAZZUP_TOKEN"))  # <-- Вставили сюда

    url = "https://api.wazzup24.com/v3/webhooks"
    headers = {
        "Authorization": f"Bearer {os.getenv('WAZZUP_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "webhooksUri": "https://bot-watsapp-bmen.onrender.com/webhook/wazzup",
        "subscriptions": {
            "messagesAndStatuses": True,
            "contactsAndDealsCreation": True,
            "channelsUpdates": True,
            "templateStatuses": True
        }
    }

    try:
        response = requests.patch(url, json=payload, headers=headers)
        print("Webhook registration response:", response.status_code)
        print("Response text:", response.text)
    except Exception as e:
        print("Exception during webhook registration:", str(e))

