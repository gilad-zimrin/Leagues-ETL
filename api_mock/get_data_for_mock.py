import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

RUN_COUNT = 3

all_apis = {
    "football_api_sports": {
        'url': os.getenv("FOOT_BALL_API_SPORTS"),
        'output_file': os.getenv("FOOTBALL_API_SPORTS_FILE"),
        'headers': {
            'x-apisports-key': os.getenv("X_APISPORTS_KEY")
        }
    }
}

current_server = "football_api_sports"
# change this to change server

API_URL = all_apis[current_server]['url']
OUTPUT_FILE = all_apis[current_server]['output_file']
headers = all_apis[current_server]['headers']




async def fetch_json(session):
    async with session.get(API_URL, headers=headers) as resp:
        print("Successfully received response")
        data = await resp.json()
        return data.get("response", [])


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
