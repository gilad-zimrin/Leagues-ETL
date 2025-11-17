import asyncio
from os import getenv
from typing import Dict, List, Any

from aiohttp import ClientSession, ClientError
from dotenv import load_dotenv

from src.models.etl_models.base_etl import BaseETL
from src.models.types.team_info import TeamInfo
from src.utils.logger import logger

load_dotenv()


class FootballApiETL(BaseETL):
    def __init__(self):
        super().__init__()
        self.current_season = getenv("FOOTBALL_API_CURRENT_SEASON")

        self.teams_url = f"{self.api_host}teams?league={self.current_league_id}&season={self.current_season}"
        self.standings_url = \
            f"{self.api_host}standings?league={self.current_league_id}&season={self.current_season}&team="
        self.headers = {
            'x-apisports-key': getenv("X_APISPORTS_KEY")
        }

    @property
    def api_host(self):
        return getenv("FOOTBALL_API_SPORTS_HOST")

    @property
    def current_league_id(self):
        return getenv("FOOTBALL_API_CURRENT_LEAGUE")

    async def extract_standing_by_team(self, raw_team: Dict[str, Dict[str, Any]]):
        """
        This function extracts the team standing by team.
        We know there is one league only because we also extract by league.
        :param raw_team: The raw 'team' and 'venue' data from the extract function.
        :return:
        """
        team_id = None
        try:
            team_id = raw_team['team']['id']
            async with ClientSession() as session:
                async with (session.get(f"{self.standings_url}{team_id}", headers=self.headers) as response):

                    logger.debug(f"Successfully received response from url f'{self.standings_url}{team_id}'", extra={
                        'etl_instance_id': self.etl_instance_id
                    })
                    raw_data = (await response.json()).get("response", [])
                    raw_standing = raw_data[0].get("league", {}) if raw_data else []
                    raw_team["league"] = raw_standing

        except (ClientError,):
            logger.exception("A client error has occurred in extract_by_team", extra={
                'etl_instance_id': self.etl_instance_id,
                'url': f"{self.standings_url}{team_id}"
            })



    async def extract(self) -> Dict | List:
        try:
            async with ClientSession() as session:
                async with session.get(self.teams_url, headers=self.headers) as response:
                    logger.debug(f"Successfully received response from url {self.teams_url}", extra={
                        'etl_instance_id': self.etl_instance_id
                    })
                    raw_teams_data: List[Dict[str, Dict[str, Any]]] = (await response.json()).get("response", [])


                await asyncio.gather(*(self.extract_standing_by_team(team) for team in raw_teams_data))

            return raw_teams_data

        except (ClientError,):
            logger.exception("A client error has occurred in extract", extra={
                'etl_instance_id': self.etl_instance_id,
            })
            raise
        except (Exception,):
            logger.exception("An unexpected error has occurred in extract", extra={
                'etl_instance_id': self.etl_instance_id,
            })
            raise


    def transform(self, raw_objects) -> List[Dict[str, Any]]:
        try:
            processed_objects = []
            for raw_object in raw_objects:
                raw_standings = raw_object['league']['standings'][0][0] if raw_object['league'] else None
                processed_objects.append(TeamInfo(
                    id=raw_object['team']['id'],
                    name=raw_object['team']['name'],
                    country=raw_object['team']['country'],
                    founded=raw_object['team']['founded'],
                    venue_name=raw_object['venue']['name'],
                    venue_address=raw_object['venue']['address'],
                    venue_city=raw_object['venue']['city'],
                    venue_capacity=raw_object['venue']['capacity'],
                    venue_surface=raw_object['venue']['surface'],
                    league_id=raw_object['league']['id'] if raw_standings else None,
                    league_name=raw_object['league']['name'] if raw_standings else None,
                    league_country=raw_object['league']['country'] if raw_standings else None,
                    rank=raw_standings['rank'],
                    points=raw_standings['points'] if raw_standings else None,
                    overall_wins=raw_standings['all']['win'] if raw_standings else None,
                    overall_loses=raw_standings['all']['draw'] if raw_standings else None,
                    overall_draws=raw_standings['all']['lose'] if raw_standings else None,
                    overall_goals_against=raw_standings['all']['goals']['for'] if raw_standings else None,
                    overall_goals_for=raw_standings['all']['goals']['against'] if raw_standings else None,
                ).model_dump())

            return processed_objects
        except (Exception,) as err:
            logger.exception(f"An unexpected error occurred in transform {str(err)}")
            raise

