from fastapi import FastAPI, Request
import httpx

from state_machine import get_state, set_state, State

app = FastAPI()

WAZZUP_TOKEN = "4e68fe2f438140b0ba531c114509b1e9"
WEBHOOK_URL = "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup"
CHANNEL_ID = "fe817b21-424e-a021-9b5200c4cf29"


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
            text = msg.get("text", "").strip()

            if not chat_id:
                print("❌ Нет chatId в сообщении.")
                continue

            print(f"📥 Получено сообщение от {chat_id}, состояние: {get_state(chat_id)}, сообщение: {text}")
            state = get_state(chat_id)

            if state == State.START:
                print(f"📊 Состояние клиента {chat_id}: START → CLIENT_TYPE")
                set_state(chat_id, State.CLIENT_TYPE)
                await send_message(chat_id,
                    "Здравствуйте! Мы поставляем оборудование для образовательных учреждений по всей России.\n"
                    "Вы представляете:\n"
                    "1️⃣ Юридическое лицо\n"
                    "2️⃣ Государственное учреждение\n"
                    "3️⃣ Физическое лицо"
                )

            elif state == State.CLIENT_TYPE:
                if text in ["1", "1️⃣", "юр", "юридическое лицо"]:
                    print(f"📊 CLIENT_TYPE → INN")
                    set_state(chat_id, State.INN)
                    await send_message(chat_id, "Хорошо, укажите, пожалуйста, ваш ИНН.")
                elif text in ["2", "2️⃣", "гос", "госучреждение"]:
                    print(f"📊 CLIENT_TYPE → GOV_INN")
                    set_state(chat_id, State.GOV_INN)
                    await send_message(chat_id, "Отлично, укажите, пожалуйста, ИНН учреждения.")
                elif text in ["3", "3️⃣", "физ", "физлицо"]:
                    print(f"📊 CLIENT_TYPE → BLOCKED")
                    set_state(chat_id, State.BLOCKED)
                    await send_message(chat_id, "Извините, мы работаем только с юрлицами и госучреждениями.")
                else:
                    await send_message(chat_id, "Пожалуйста, выберите 1️⃣, 2️⃣ или 3️⃣.")

            elif state == State.BLOCKED:
                print(f"🔒 {chat_id} в состоянии BLOCKED — игнорируем.")

            # Можно добавить elif'ы под следующие шаги

    except Exception as e:
        print("❌ Ошибка обработки webhook:", str(e))

    return {"message": "Получено"}


# Отправка сообщений через Wazzup
async def send_message(chat_id: str, text: str):
    url = "https://api.wazzup24.com/v3/message"
    headers = {
        "Authorization": f"Bearer {WAZZUP_TOKEN}",
        "Content-Type": "application/json"
    }

    # Приведение chat_id к формату chatId Wazzup (например: 79651234567@c.us)
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

