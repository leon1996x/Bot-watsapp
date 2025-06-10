
import requests

WEBHOOK_URL = "https://bot-watsapp-bmen.onrender.com/webhook/wazzup"
TOKEN = "4e68fe2f438140b0ba531c114509b1e9"

response = requests.post(
    "https://api.wazzup24.com/v3/channels/register-webhook",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={"url": WEBHOOK_URL}
)

if response.status_code == 200:
    print("Webhook успешно зарегистрирован")
else:
    print("Ошибка при регистрации webhook:", response.status_code, response.text)
