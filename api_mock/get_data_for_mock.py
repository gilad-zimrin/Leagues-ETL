import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

RUN_COUNT = 1

mock_request_action = os.getenv("MOCK_REQUEST_ACTION")


all_apis = {
    "football_api_sports": {
        'host': os.getenv("FOOTBALL_API_SPORTS_HOST"),
        'route': mock_request_action,
        'output_file': f'{os.getenv("FOOTBALL_API_SPORTS_FILE")}_{mock_request_action}.json',
        'parameters': f'?league={int(os.getenv("FOOTBALL_API_CURRENT_LEAGUE"))}&season={int(os.getenv("FOOTBALL_API_CURRENT_SEASON"))}',
        'headers': {
            'x-apisports-key': os.getenv("X_APISPORTS_KEY")
        }
    },
    "api_football": {
        'host': os.getenv("API_FOOTBALL_HOST"),
        'route': '',
        'output_file': f'{os.getenv("API_FOOTBALL_SPORTS_FILE")}_{mock_request_action}.json',
        'parameters': f'?action=get_{mock_request_action}&league_id={int(os.getenv("API_FOOTBALL_CURRENT_LEAGUE"))}&APIkey={os.getenv("API_FOOTBALL_TOKEN")}',
        'headers': {}
    }
}

current_server = "football_api_sports"
# change this to change server

api_url = f'{all_apis[current_server]['host']}{all_apis[current_server]['route']}{all_apis[current_server]['parameters']}'
OUTPUT_FILE = all_apis[current_server]['output_file']
headers = all_apis[current_server]['headers']




async def fetch_json(session):
    async with session.get(api_url, headers=headers) as resp:
        print(f"Successfully received response from url {api_url}")
        data = await resp.json()
        return data


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
