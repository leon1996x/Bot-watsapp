
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def register():
    token = os.getenv("WAZZUP_TOKEN")
    print(f"🔑 TOKEN: {token}")

    url = "https://api.wazzup24.com/v3/webhooks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "webhooksUri": "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup",
        "subscriptions": {
            "messagesAndStatuses": True,
            "contactsAndDealsCreation": True,
            "channelsUpdates": True,
            "templateStatuses": True
        }
    }

    try:
        response = requests.patch(url, json=payload, headers=headers)
        print("📡 Webhook registration response:", response.status_code)
        print("📬 Response text:", response.text)
        return {
            "status_code": response.status_code,
            "response": response.json()
        }
    except Exception as e:
        print("❌ Exception during webhook registration:", str(e))
        return {"error": str(e)}
