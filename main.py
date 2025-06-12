from fastapi import FastAPI, Request
import httpx

from state_machine import get_state, set_state, State

app = FastAPI()

WAZZUP_TOKEN = "4e68fe2f438140b0ba531c114509b1e9"
WEBHOOK_URL = "https://bot-watsapp-y7e8.onrender.com/webhook/wazzup"
CHANNEL_ID = "fe817b21-47a7-424e-a021-9b5200c4cf29"


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
            text = msg.get("text", "").strip()
            phone = msg.get("contact", {}).get("phone")
            chat_id = msg.get("chatId", "")

            # если номера нет — пробуем вытащить из chatId
            if not phone and chat_id and chat_id[-10:].isdigit():
                phone = "+7" + chat_id[-10:]

            if not phone:
                print("❌ Не удалось определить номер телефона.")
                continue

            print(f"📞 phone: {phone}, 💬 сообщение: {text}")

            state = get_state(phone)

            if state == State.START:
                await send_message(phone, 
                    "Здравствуйте! Мы поставляем оборудование для образовательных учреждений по всей России.\n"
                    "Вы представляете:\n"
                    "1️⃣ Юридическое лицо\n"
                    "2️⃣ Государственное учреждение\n"
                    "3️⃣ Физическое лицо", 
                    chat_id
                )
                set_state(phone, State.CLIENT_TYPE)

            elif state == State.CLIENT_TYPE:
                if text in ["1", "1️⃣", "юр", "юридическое лицо"]:
                    await send_message(phone, "Хорошо, укажите, пожалуйста, ваш ИНН.", chat_id)
                    set_state(phone, State.INN)
                elif text in ["2", "2️⃣", "гос", "госучреждение"]:
                    await send_message(phone, "Отлично, укажите, пожалуйста, ИНН учреждения.", chat_id)
                    set_state(phone, State.GOV_INN)
                elif text in ["3", "3️⃣", "физ", "физлицо"]:
                    await send_message(phone, "Извините, мы работаем только с юрлицами и госучреждениями.", chat_id)
                    set_state(phone, State.START)
                else:
                    await send_message(phone, "Пожалуйста, выберите 1️⃣, 2️⃣ или 3️⃣.", chat_id)

    except Exception as e:
        print("❌ Ошибка обработки webhook:", str(e))

    return {"message": "Получено"}


# ✅ send_message с поддержкой chatId
async def send_message(phone: str, text: str, chat_id: str = None):
    url = "https://api.wazzup24.com/v3/message"
    headers = {
        "Authorization": f"Bearer {WAZZUP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "channelId": CHANNEL_ID,
        "text": text
    }

    if chat_id:
        data["chatId"] = chat_id
    else:
        data["chatType"] = "whatsapp"
        data["phone"] = phone

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
