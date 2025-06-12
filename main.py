from fastapi import FastAPI, Request
import httpx

from state_machine import (
    get_state, set_state, State,
    get_last_message, set_last_message
)

app = FastAPI()

WAZZUP_TOKEN = ""
WEBHOOK_URL = "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup"
CHANNEL_ID = "fe817b21-47a7-a021-9b5200c4cf29"


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
            chat_id = msg.get("chatId", "").strip()
            text = msg.get("text", "").strip().lower()

            if not chat_id:
                print("❌ Нет chatId в сообщении.")
                continue

            print(f"👤 chatId: {chat_id}, 💬 сообщение: {text}")

            state = get_state(chat_id)

            if state == State.START:
                await send_message(chat_id,
                    "Здравствуйте! Мы поставляем оборудование для образовательных учреждений по всей России.\n"
                    "Вы представляете:\n"
                    "1️⃣ Юридическое лицо\n"
                    "2️⃣ Государственное учреждение\n"
                    "3️⃣ Физическое лицо"
                )
                set_state(chat_id, State.CLIENT_TYPE)

            elif state == State.CLIENT_TYPE:
                if text in ["1", "1️⃣", "юр", "юридическое лицо"]:
                    await send_message(chat_id, "Хорошо, укажите, пожалуйста, ваш ИНН.")
                    set_state(chat_id, State.INN)
                elif text in ["2", "2️⃣", "гос", "госучреждение", "государственное учреждение"]:
                    await send_message(chat_id, "Отлично, укажите, пожалуйста, ИНН учреждения.")
                    set_state(chat_id, State.GOV_INN)
                elif text in ["3", "3️⃣", "физ", "физлицо", "физическое лицо"]:
                    await send_message(chat_id, "Извините, мы работаем только с юридическими лицами и государственными учреждениями.")
                    set_state(chat_id, State.BLOCKED)
                else:
                    await send_message(chat_id, "Пожалуйста, выберите 1️⃣, 2️⃣ или 3️⃣.")

    except Exception as e:
        print("❌ Ошибка обработки webhook:", str(e))

    return {"message": "Получено"}


# ✅ УСТОЙЧИВАЯ отправка сообщений через Wazzup (без спама)
async def send_message(chat_id: str, text: str):
    if get_last_message(chat_id) == text:
        print(f"⚠️ Повторное сообщение не отправлено для {chat_id}")
        return

    url = "https://api.wazzup24.com/v3/message"
    headers = {
        "Authorization": f"Bearer {WAZZUP_TOKEN}",
        "Content-Type": "application/json"
    }

    if not chat_id.endswith("@c.us"):
        chat_id = chat_id.replace("+", "").replace("@c.us", "") + "@c.us"

    data = {
        "channelId": CHANNEL_ID,
        "chatId": chat_id,
        "chatType": "whatsapp",
        "text": text
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    print("📤 Ответ Wazzup:", response.status_code, await response.aread())
    set_last_message(chat_id, text)


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
