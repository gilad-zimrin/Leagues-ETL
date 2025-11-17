from asyncio import Event, run
from datetime import datetime
from os import getenv
from threading import Thread

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import app
from models.etl_models.api_football import APIFootballETL
from models.etl_models.football_api_etl import FootballApiETL
from src.utils.logger import logger

scheduler_interval_minutes = int(getenv("SCHEDULER_INTERVAL_MINUTES", default=60))

# This variable holds all the data sources the server works with, with the interval they should run with
all_data_sources_etls = [
    (FootballApiETL(), scheduler_interval_minutes * 60),
    (APIFootballETL(), scheduler_interval_minutes * 60)
]

def run_fast_api_app():
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=int(getenv("APP_PORT", default=4000)),
    )
    logger.info("FastAPI app starting up..")



async def run_scheduler():
    scheduler = AsyncIOScheduler()
    for source_etl in all_data_sources_etls:
        scheduler.add_job(
            source_etl[0].execute,
            'interval',
            seconds=source_etl[1],
            next_run_time=datetime.now(),
        )
    scheduler.start()
    logger.info("FastAPI app starting up..")

    Thread(target=run_fast_api_app).start()

    try:
        await Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass

def main():
    try:
        run(run_scheduler())
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
