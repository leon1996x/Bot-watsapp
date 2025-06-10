from fastapi import FastAPI, Request, Response
from dialog_state import process_message
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Удалили register() из startup, чтобы вручную вызывать через /register
@app.on_event("startup")
async def startup_event():
    print("🚀 Приложение запущено!")

# Проверка доступности главной страницы
@app.get("/")
@app.head("/")
async def root():
    return {"status": "ok"}

# Обработка Webhook Wazzup — логируем все входящие запросы
@app.post("/webhook/wazzup")
@app.head("/webhook/wazzup")
async def wazzup_webhook(request: Request):
    print(f"📩 Получен запрос: {request.method}")
    try:
        data = await request.json()
        print("📦 Получен JSON:", data)
    except Exception as e:
        print("❌ Ошибка при разборе JSON:", str(e))
        return Response(status_code=200)  # Возвращаем 200 даже при ошибке

    # Если в сообщении есть данные — обрабатываем
    messages = data.get("messages", [])
    for msg in messages:
        phone = msg["author"].replace("whatsapp:", "")
        text = msg.get("text", "")
        await process_message(phone, text)

    return {"status": "ok"}

# Ручная регистрация вебхука
@app.get("/register")
async def trigger_register():
    from register_webhook import register
    register()
    return {"status": "Webhook registration triggered"}
