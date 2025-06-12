from fastapi import FastAPI, Request
import httpx
from state_machine import State, get_state, set_state, user_data
import os

app = FastAPI()

WAZZUP_TOKEN = os.getenv("WAZZUP_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # например: "fe817b21-47a7-424e-a021-9b5200c4cf29"


async def send_message(chat_id: str, text: str):
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


@app.post("/webhook/wazzup")
async def handle_webhook(request: Request):
    body = await request.json()
    print("📩 Webhook получен:", body)

    for msg in body.get("messages", []):
        # 🔒 Игнорируем сообщения от самого бота (echo или direction != "in")
        if msg.get("isEcho") or msg.get("direction") != "in":
            print("↪ Пропущено сообщение: echo или не входящее")
            continue

        chat_id = msg.get("chatId", "").strip()
        text = msg.get("text", "").strip().lower()

        if not chat_id or not text:
            print("❌ Нет chat_id или текста.")
            continue

        print(f"👤 chatId: {chat_id}, 💬 сообщение: {text}")

        state = get_state(chat_id)

        # FSM: логика по состояниям
        if state == State.START:
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
                set_state(chat_id, State.INN)
                await send_message(chat_id, "Хорошо, укажите, пожалуйста, ваш ИНН.")
            elif text in ["2", "2️⃣", "гос", "госучреждение"]:
                set_state(chat_id, State.GOV_INN)
                await send_message(chat_id, "Отлично, укажите, пожалуйста, ИНН учреждения.")
            elif text in ["3", "3️⃣", "физ", "физлицо"]:
                set_state(chat_id, State.BLOCKED)
                await send_message(chat_id, "Извините, мы работаем только с юрлицами и госучреждениями.")
            else:
                await send_message(chat_id, "Пожалуйста, выберите 1️⃣, 2️⃣ или 3️⃣.")

    return {"status": "ok"}
