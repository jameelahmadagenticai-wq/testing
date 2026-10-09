from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from agent import autonomous_agent
import asyncio
from slack import send_to_slack

app = FastAPI()

async def stream_agent(topic: str):
    summary, logs = autonomous_agent(topic)

    for log in logs:
        yield log + "\n"
        await asyncio.sleep(0.2)

    yield "\n📌 FINAL SUMMARY:\n"
    yield summary

@app.get("/analyze")
async def analyze(topic: str):
    return StreamingResponse(stream_agent(topic), media_type="text/plain")



@app.get("/analyze-slack")
async def analyze_and_send(topic: str):
    summary, logs = autonomous_agent(topic)

    await send_to_slack(f"*Topic:* {topic}\n\n{summary}")

    return {"status": "sent to slack"}