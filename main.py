from fastapi import FastAPI, Request, Response
from dialog_state import process_message
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

WAZZUP_API_TOKEN = os.getenv("WAZZUP_TOKEN")

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("🔥 THIS IS THE RIGHT MAIN.PY")
    print("🚀 Приложение запущено!")


@app.get("/")
@app.head("/")
async def root():
    return {"status": "ok"}


@app.post("/webhook/wazzup")
@app.head("/webhook/wazzup")
async def wazzup_webhook(request: Request):
    if request.method == "HEAD":
        return Response(status_code=200)
    try:
        data = await request.json()
        print("📩 Webhook получен:", data)
        messages = data.get("messages", [])
        for msg in messages:
            phone = msg["author"].replace("whatsapp:", "")
            text = msg.get("text", "")
            await process_message(phone, text)
    except Exception as e:
        print("❌ Ошибка обработки webhook:", str(e))
    return {"status": "ok"}


@app.get("/register")
async def register_webhook():
    print("Регистрируем вебхук...")
    headers = {
        "Authorization": f"Bearer {WAZZUP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "webhooksUri": "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup",
        "subscriptions": {
            "messagesAndStatuses": True,
            "contactsAndDealsCreation": True
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch("https://api.wazzup24.com/v3/webhooks", headers=headers, json=data)

    print(f"📡 Webhook registration response: {response.status_code}")
    print(f"📬 Response text: {response.text}")

    try:
        json_data = response.json() if response.content else {"message": "Empty response"}
    except Exception as e:
        json_data = {"error": "Failed to parse JSON", "details": str(e)}

    return {
        "status_code": response.status_code,
        "response": json_data
    }

