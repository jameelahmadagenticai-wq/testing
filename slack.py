import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

async def send_to_slack(message: str):
    if not SLACK_WEBHOOK:
        print("❌ Slack webhook not found")
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SLACK_WEBHOOK,
                json={"text": message}
            )
            print("Slack response:", response.status_code)

    except Exception as e:
        print("Slack error:", str(e))