import json
from bitrix import send_to_bitrix

users = {}

async def process_message(phone: str, text: str):
    state = users.get(phone, {"step": "start", "data": {}})

    if state["step"] == "start":
        if text.lower() in ["1", "юрлицо", "юридическое лицо"]:
            state["data"]["Тип клиента"] = "Юрлицо"
            state["step"] = "get_inn"
            send_msg(phone, "Введите ИНН организации:")
        elif text.lower() in ["2", "госучреждение"]:
            state["data"]["Тип клиента"] = "Госучреждение"
            state["step"] = "get_inn"
            send_msg(phone, "Введите ИНН учреждения:")
        else:
            send_msg(phone, "Выберите 1️⃣ Юрлицо или 2️⃣ Госучреждение")

    elif state["step"] == "get_inn":
        state["data"]["ИНН"] = text
        state["step"] = "get_goal"
        send_msg(phone, "Для чего приобретается оборудование?\n1. Для себя\n2. Торги\n3. Поставка в госучреждение")

    elif state["step"] == "get_goal":
        goals = {"1": "Для себя", "2": "Торги", "3": "Поставка в гос"}
        if text in goals:
            state["data"]["Цель закупки"] = goals[text]
            state["step"] = "get_contacts"
            send_msg(phone, "Оставьте номер телефона и email:")
        else:
            send_msg(phone, "Выберите 1, 2 или 3")

    elif state["step"] == "get_contacts":
        state["data"]["Контакты"] = text
        send_to_bitrix(state["data"])
        send_msg(phone, "Спасибо! Заявка передана менеджеру.")
        users.pop(phone)
        return

    users[phone] = state

def send_msg(phone: str, text: str):
    # TODO: здесь должен быть запрос в Wazzup API
    print(f"[{phone}] {text}")