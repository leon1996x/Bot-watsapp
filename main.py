# main.py
from fastapi import FastAPI, Request
import httpx
from state_machine import get_state, set_state, State, get_context, update_context

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    print("🔥 FSM бот запущен")

@app.get("/")
async def root():
    return {"message": "Бот работает!"}

@app.get("/webhook/wazzup")
@app.head("/webhook/wazzup")
async def wazzup_webhook_check():
    return {"status": "ok"}

@app.post("/webhook/wazzup")
async def handle_webhook(request: Request):
    body = await request.json()
    print("📩 Webhook получен:", body)

    for msg in body.get("messages", []):
        chat_id = msg.get("chatId", "").strip()
        text = msg.get("text", "").strip().lower()

        if not chat_id:
            continue

        state = get_state(chat_id)
        context = get_context(chat_id)

        if state == State.START:
            await send_message(chat_id, "Здравствуйте! Мы поставляем оборудование для образовательных учреждений по всей России.\nКем вы являетесь? (юридическое лицо / государственное учреждение / физическое лицо)")
            set_state(chat_id, State.CLIENT_TYPE)

        elif state == State.CLIENT_TYPE:
            if "физ" in text:
                await send_message(chat_id, "Извините, мы работаем только с юридическими лицами и государственными учреждениями. Спасибо за понимание!")
                set_state(chat_id, State.START)
            elif "юр" in text:
                update_context(chat_id, {"client_type": "juridical"})
                await send_message(chat_id, "Пожалуйста, укажите ИНН вашей организации")
                set_state(chat_id, State.INN)
            elif "гос" in text or "учреждение" in text:
                update_context(chat_id, {"client_type": "gov"})
                await send_message(chat_id, "Пожалуйста, укажите ИНН учреждения")
                set_state(chat_id, State.INN)
            else:
                await send_message(chat_id, "Пожалуйста, уточните: юридическое лицо, государственное учреждение или физическое лицо?")

        elif state == State.INN:
            update_context(chat_id, {"inn": text})
            if context.get("client_type") == "juridical":
                await send_message(chat_id, "Для чего приобретается оборудование? (для собственного использования / для участия в торгах / для поставки в госучреждение)")
                set_state(chat_id, State.PURPOSE)
            else:
                await send_message(chat_id, "Как будет проводиться закупка? (прямой контракт / через торги)")
                set_state(chat_id, State.GOV_PURCHASE_METHOD)

        elif state == State.PURPOSE:
            update_context(chat_id, {"purpose": text})
            if "торг" in text:
                await send_message(chat_id, "Благодарим! Мы можем помочь с подготовкой коммерческого предложения. Эта информация поможет актуализировать цены и сроки поставки.")
            if "гос" in text:
                await send_message(chat_id, "Укажите, пожалуйста, ИНН госучреждения")
                set_state(chat_id, State.GOV_PARTNER_INN)
                return
            await send_message(chat_id, "Укажите планируемые сроки закупки")
            set_state(chat_id, State.DEADLINE)

        elif state == State.GOV_PURCHASE_METHOD:
            update_context(chat_id, {"gov_method": text})
            if "прямой" in text:
                await send_message(chat_id, "Вы можете оформить заявку прямо в чате. Также можете отправить заявку на нашу почту.")
            else:
                await send_message(chat_id, "Мы можем помочь в составлении технического задания для аукциона.")
            await send_message(chat_id, "Требуется ли монтаж оборудования и обучение персонала?")
            set_state(chat_id, State.EXTRA_SERVICES)

        elif state == State.GOV_PARTNER_INN:
            update_context(chat_id, {"gov_partner_inn": text})
            await send_message(chat_id, "Укажите планируемые сроки закупки")
            set_state(chat_id, State.DEADLINE)

        elif state == State.DEADLINE:
            update_context(chat_id, {"deadline": text})
            await send_message(chat_id, "Оставьте, пожалуйста, номер телефона и email для связи")
            set_state(chat_id, State.CONTACTS)

        elif state == State.EXTRA_SERVICES:
            update_context(chat_id, {"extra_services": text})
            await send_message(chat_id, "Укажите планируемые сроки закупки")
            set_state(chat_id, State.DEADLINE)

        elif state == State.CONTACTS:
            update_context(chat_id, {"contacts": text})
            await send_message(chat_id, "Спасибо! Ваши данные переданы менеджеру. Он свяжется с вами в ближайшее время.")
            set_state(chat_id, State.START)

    return {"message": "ok"}

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
        await client.post(url, json=data, headers=headers)  # игнорируем ответ ради скорости
