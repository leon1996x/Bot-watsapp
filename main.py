# main.py — заглушка
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Бот временно отключён."}

@app.post("/webhook/wazzup")
def ignore_webhook():
    # Просто игнорируем все входящие запросы
    return {"status": "ok"}
