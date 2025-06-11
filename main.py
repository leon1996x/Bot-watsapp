
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

WAZZUP_TOKEN = "4e68fe2f438140b0ba531c114509b1e9"
WEBHOOK_URL = "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup"  # Убедись, что этот адрес совпадает с Render URL

@app.on_event("startup")
async def startup_event():
    print("🔥 THIS IS THE RIGHT MAIN.PY")
    print("🚀 Приложение запущено!")

@app.get("/")
async def root():
    return {"message": "Приложение работает!"}

# ✅ Новый обработчик: GET и HEAD на /webhook/wazzup
@app.get("/webhook/wazzup")
@app.head("/webhook/wazzup")
async def wazzup_webhook_check():
    return {"status": "ok"}

@app.post("/webhook/wazzup")
async def handle_webhook(request: Request):
    body = await request.json()
    print("📩 Webhook получен:", body)
    return {"message": "Получено"}

@app.get("/register")
async def register_webhook():
    print("Регистрируем вебхук...")
    print("🔑 TOKEN:", WAZZUP_TOKEN)

    url = "https://api.wazzup24.com/v3/webhooks"
    headers = {
        "Authorization": f"Bearer {WAZZUP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "webhooksUri": WEBHOOK_URL,
        "subscriptions": {
            "messagesAndStatuses": True,
            "contactsAndDealsCreation": True
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=data, headers=headers)

    print("📡 Webhook registration response:", response.status_code)
    print("📬 Response text:", response.text)

    return {
        "status_code": response.status_code,
        "response": response.json()
    }
