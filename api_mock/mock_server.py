from fastapi import FastAPI, HTTPException
import json
import os
import random
import uvicorn

FILE_PATH = "football_api_sports.json"

app = FastAPI()


def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)


@app.get("/leagues")
def get_mock_football_api_sports():
    data = load_data()
    if not data:
        raise HTTPException(status_code=404, detail="No data available")
    return random.choice(data)


uvicorn.run(
    app=app,
    host='0.0.0.0',
    port=int(os.getenv("MOCK_PORT", default=4044)),
)
