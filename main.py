from fastapi import FastAPI, Request
import httpx
import os

from state_machine import get_state, set_state, State  # <-- добавляем FSM

app = FastAPI()

WAZZUP_TOKEN = "4e68fe2f438140b0ba531c114509b1e9"
WEBHOOK_URL = "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup"

@app.on_event("startup")
async def startup_event():
    print("🔥 THIS IS THE RIGHT MAIN.PY")
    print("🚀 Приложение запущено!")

@app.get("/")
async def root():
    return {"message": "Приложение работает!"}

@app.get("/webhook/wazzup")
@app.head("/webhook/wazzup")
async def wazzup_webhook_check():
    return {"status": "ok"}

@app.post("/webhook/wazzup")
async def handle_webhook(request: Request):
    body = await request.json()
    print("📩 Webhook получен:", body)

    try:
        for msg in body.get("messages", []):
            chat_id = msg.get("chatId")
            text = msg.get("text", "").strip()
            print(f"👤 chatId: {chat_id}, 💬 сообщение: {text}")

            state = get_state(chat_id)

            if state == State.START:
                # Первый шаг: спрашиваем тип клиента
                await send_message(chat_id, 
                    "Здравствуйте! Мы поставляем оборудование для образовательных учреждений по всей России.\n"
                    "Вы представляете:\n"
                    "1️⃣ Юридическое лицо\n"
                    "2️⃣ Государственное учреждение\n"
                    "3️⃣ Физическое лицо"
                )
                set_state(chat_id, State.ASK_CLIENT_TYPE)

            elif state == State.ASK_CLIENT_TYPE:
                # Обработка ответа на вопрос "Кто вы?"
                if text in ["1", "1️⃣", "юр", "юридическое лицо"]:
                    await send_message(chat_id, "Хорошо, укажите, пожалуйста, ваш ИНН.")
                    set_state(chat_id, State.ASK_INN)
                elif text in ["2", "2️⃣", "гос", "госучреждение"]:
                    await send_message(chat_id, "Отлично, укажите, пожалуйста, ИНН учреждения.")
                    set_state(chat_id, State.ASK_INN)
                elif text in ["3", "3️⃣", "физ", "физлицо"]:
                    await send_message(chat_id, 
                        "Извините, мы работаем только с юрлицами и госучреждениями.")
                    set_state(chat_id, State.START)  # сбрасываем
                else:
                    await send_message(chat_id, "Пожалуйста, выберите 1️⃣, 2️⃣ или 3️⃣.")

            # добавим остальные шаги позже

    except Exception as e:
        print("❌ Ошибка обработки webhook:", str(e))

    return {"message": "Получено"}

# Функция для отправки сообщений через Wazzup
async def send_message(chat_id: str, text: str):
    url = "https://api.wazzup24.com/v3/message"
    headers = {
        "Authorization": f"Bearer {WAZZUP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "chatId": chat_id,
        "text": text
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    print("📤 Ответ Wazzup:", response.status_code, await response.aread())

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

    try:
        json_response = response.json()
    except Exception as e:
        return {
            "status_code": response.status_code,
            "response": {
                "error": "Failed to parse JSON",
                "details": str(e)
            }
        }

    return {
        "status_code": response.status_code,
        "response": json_response
    }

