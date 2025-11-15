import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

API_URL = "https://v3.football.api-sports.io/leagues"
OUTPUT_FILE = "football_api_sports.json"
RUN_COUNT = 8

load_dotenv()

x_apisports_key = os.getenv("X_APISPORTS_KEY")

headers = {
    'x-apisports-key': x_apisports_key
    }


async def fetch_json(session):
    print(headers)
    async with session.get(API_URL, headers=headers) as resp:
        print(resp)
        return await resp.json()


def load_existing_data():
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r") as f:
        if f:
            return json.load(f)
        raise ValueError("data file empty")


def save_data(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)


async def main():
    existing = load_existing_data()

    async with aiohttp.ClientSession() as session:
        for _ in range(RUN_COUNT):
            result = await fetch_json(session)
            existing.append(result)

    save_data(existing)


if __name__ == "__main__":
    asyncio.run(main())
