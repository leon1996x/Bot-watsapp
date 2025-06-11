
from fastapi import FastAPI, Request, Response
from dialog_state import process_message
import os
from dotenv import load_dotenv
from register_webhook import register

load_dotenv()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("🔥 THIS IS THE RIGHT MAIN.PY")
    print("🚀 Приложение запущено!")

@app.get("/")
@app.head("/")
async def root():
    return {"status": "ok"}

@app.api_route("/webhook/wazzup", methods=["POST", "HEAD"])
async def wazzup_webhook(request: Request):
    if request.method == "HEAD":
        print("✅ HEAD-запрос от Wazzup получен")
        return Response(status_code=200)
    data = await request.json()
    messages = data.get("messages", [])
    for msg in messages:
        phone = msg["author"].replace("whatsapp:", "")
        text = msg.get("text", "")
        await process_message(phone, text)
    return {"status": "ok"}

@app.get("/register")
async def trigger_register():
    print("🔁 Регистрируем вебхук...")
    result = register()
    return result
