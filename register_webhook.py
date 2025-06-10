import requests
import os
from dotenv import load_dotenv

load_dotenv()

def register():
    url = "https://api.wazzup24.com/v3/webhooks"
    token = os.getenv("WAZZUP_TOKEN")

    print("🔑 TOKEN:", token)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "webhooksUri": "https://bot-watsapp-bmen.onrender.com/webhook/wazzup",
        "subscriptions": {
            "messagesAndStatuses": True,
            "contactsAndDealsCreation": True,
            "channelsUpdates": True,
            "templateStatus": True  # ВАЖНО: должно быть "templateStatus", а не "templateStatuses"
        }
    }

    try:
        response = requests.patch(url, json=payload, headers=headers)
        print("📡 Webhook registration response:", response.status_code)
        print("📬 Response text:", response.text)
    except Exception as e:
        print("❌ Exception during webhook registration:", str(e))
