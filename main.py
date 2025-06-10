from fastapi import FastAPI, Request, Response
import json

app = FastAPI()

@app.get("/")
@app.head("/")
async def root():
    return Response(status_code=200)

@app.head("/webhook/wazzup")
async def wazzup_webhook_head():
    return Response(status_code=200)

@app.options("/webhook/wazzup")
async def wazzup_webhook_options():
    return Response(status_code=200)

@app.post("/webhook/wazzup")
async def wazzup_webhook(request: Request):
    # Простой ответ без обработки тела
    return Response(content=json.dumps({"status": "ok"}), media_type="application/json")
