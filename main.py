from fastapi import FastAPI, Request
from dialog_state import process_message
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    from register_webhook import register
    register()

@app.post("/webhook/wazzup")
async def wazzup_webhook(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    for msg in messages:
        phone = msg["author"].replace("whatsapp:", "")
        text = msg.get("text", "")
        await process_message(phone, text)
    return {"status": "ok"}
