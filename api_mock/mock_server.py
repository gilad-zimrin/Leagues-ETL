from fastapi import FastAPI, HTTPException
import json
import os
import random
import uvicorn



app = FastAPI()


def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)


@app.get("/football_api_teams")
def get_mock_football_api_sports():
    data = load_data('football_api_sports_teams.json')
    if not data:
        raise HTTPException(status_code=404, detail="No data available")
    return random.choice(data)


@app.get("/football_api_standings")
def get_mock_football_api_sports():
    data = load_data('football_api_sports_standings.json')
    if not data:
        raise HTTPException(status_code=404, detail="No data available")
    return random.choice(data)


uvicorn.run(
    app=app,
    host='0.0.0.0',
    port=int(os.getenv("MOCK_PORT", default=4044)),
)
