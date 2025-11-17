from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI

from models.big_query_handler import BigQueryHandler

load_dotenv()

project_id = getenv("BIGQUERY_PROJECT_ID")
team_info_table = getenv('TEAM_INFO_TABLE')

def create_app():
    app = FastAPI()

    app.state.bigquery = BigQueryHandler()

    @app.get("/all_team_info")
    def get_all_team_info():
        return app.state.bigquery.get_all(f"{project_id}.{team_info_table}")

    # Easy to make more querying/filtering routes

    return app


app = create_app()
