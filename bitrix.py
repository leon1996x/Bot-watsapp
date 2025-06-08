import os
import requests

BITRIX_WEBHOOK = os.getenv("BITRIX_WEBHOOK")

def send_to_bitrix(data: dict):
    payload = {
        "fields": {
            "TITLE": "Новый лид из WhatsApp",
            "UF_CRM_1700000001": data.get("Тип клиента"),
            "UF_CRM_1700000002": data.get("ИНН"),
            "UF_CRM_1700000003": data.get("Цель закупки"),
            "UF_CRM_1700000004": data.get("Контакты"),
            "STATUS_ID": "NEW"
        }
    }
    url = f"{BITRIX_WEBHOOK}crm.lead.add.json"
    response = requests.post(url, json=payload)
    print("Bitrix ответ:", response.json())