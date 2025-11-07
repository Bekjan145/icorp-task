import asyncio
import logging
import os
from contextlib import asynccontextmanager

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL must be set in .env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started. Running solve() task...")
    asyncio.create_task(solve())
    yield


app = FastAPI(lifespan=lifespan)


class Payload(BaseModel):
    msg: str
    url: str


class CodePart(BaseModel):
    part2: str | None = None


second_part: str | None = None
second_part_ready = asyncio.Event()


@app.post("/webhook")
async def webhook(data: CodePart):
    global second_part
    second_part = data.part2
    second_part_ready.set()
    return {"ok": True}


async def solve():
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = Payload(msg="Hello iCorp!", url=WEBHOOK_URL)

        try:
            r1 = await client.post("https://test.icorp.uz/interview.php",
                                   json=payload.model_dump())
            r1.raise_for_status()
            data = r1.json()
        except Exception as e:
            logger.error(f"Error in POST request: {e}")
            return

        first = data.get("part1")
        if not first:
            logger.warning("The first part is not received")
            return

        logger.info(f"PART 1: {first}")

        try:
            await asyncio.wait_for(second_part_ready.wait(), timeout=60)
        except asyncio.TimeoutError:
            logger.error("The second part did not arrive on time")
            return

        if not second_part:
            logger.error("The second part is empty")
            return

        logger.info(f"PART 2: {second_part}")

        full_code = first + second_part
        logger.info(f"FULL CODE: {full_code}")

        try:
            r2 = await client.get("https://test.icorp.uz/interview.php",
                                  params={"code": full_code})
            r2.raise_for_status()
            result = r2.json()
        except Exception as e:
            logger.error(f"Error in final GET request: {e}")
            return

        final_message = result.get("msg")
        if not final_message:
            logger.warning("Final message not found")
            return

        logger.info(f"FINAL MESSAGE: {final_message}")


if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
