from os import getenv
from typing import Dict, List, Any

from aiohttp import ClientSession, ClientError
from dotenv import load_dotenv

from models.etl_models.base_etl import BaseETL
from models.types.team_info import TeamInfo
from utils.logger import logger

load_dotenv()


class APIFootballETL(BaseETL):
    def __init__(self):
        super().__init__()
        self.teams_url = \
            f"{self.api_host}?action=get_teams&league_id={self.current_league_id}&APIkey={getenv('API_FOOTBALL_TOKEN')}"
        self.standings_url = (f"{self.api_host}?action=get_standings&league_id="
                              f"{self.current_league_id}&APIkey={getenv('API_FOOTBALL_TOKEN')}")

    @property
    def api_host(self):
        return getenv("API_FOOTBALL_HOST")

    @property
    def current_league_id(self):
        return getenv("API_FOOTBALL_CURRENT_LEAGUE")


    async def extract(self) -> Dict | List:
        try:
            async with ClientSession() as session:
                async with session.get(self.teams_url) as response:
                    logger.debug(f"Successfully received response from url {self.teams_url}", extra={
                        'etl_instance_id': self.etl_instance_id
                    })
                    raw_teams_data: List[Dict[str, Dict[str, Any]]] = await response.json()
                    [raw_team.pop('players') for raw_team in raw_teams_data]

                    print(raw_teams_data)

                async with session.get(self.standings_url) as response:
                    logger.debug(f"Successfully received response from url {self.teams_url}", extra={
                        'etl_instance_id': self.etl_instance_id
                    })
                    raw_standings_data: List[Dict[str, Dict[str, Any]]] = await response.json()
                    print(raw_standings_data)


            return {
                'raw_teams': raw_teams_data,
                'raw_standings': raw_standings_data
            }

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

    @staticmethod
    def merge_teams(raw_teams, raw_standings):
        """
        This function merges the data from raw_teams and raw_standings by team_id and team_key
        :param raw_teams:
        :param raw_standings:
        :return:
        """
        merged_teams = []
        lookup_dict = {raw_standing['team_id']: raw_standing for raw_standing in raw_standings}

        for raw_team in raw_teams:
            key = raw_team['team_key']
            if key in lookup_dict:
                merged_team = {**raw_team, **lookup_dict[key]}
                merged_teams.append(merged_team)
        return merged_teams

    def transform(self, raw_data) -> List[Dict[str, Any]]:
        merged_teams = self.merge_teams(raw_data['raw_teams'], raw_data['raw_standings'])
        processed_objects = []

        for raw_object in merged_teams:
            print(raw_object)
            processed_objects.append(TeamInfo(
                id=int(raw_object['team_key']),
                name=raw_object['team_name'],
                country=raw_object['team_country'],
                founded=raw_object['team_founded'] if raw_object['team_founded'] else None,
                venue_name=raw_object['venue']['venue_name'] if raw_object['venue'] else None,
                venue_address=raw_object['venue']['venue_address'] if raw_object['venue'] else None,
                venue_city=raw_object['venue']['venue_city'] if raw_object['venue'] else None,
                venue_capacity=int(raw_object['venue']['venue_capacity']) if raw_object['venue'] else None,
                venue_surface=raw_object['venue']['venue_surface'] if raw_object['venue'] else None,
                league_id=int(raw_object['league_id']),
                league_name=raw_object['league_name'],
                league_country=raw_object['country_name'],
                rank=int(raw_object['overall_league_position']),
                points=int(raw_object['overall_league_PTS']),
                overall_wins=int(raw_object['overall_league_W']),
                overall_loses=int(raw_object['overall_league_L']),
                overall_draws=int(raw_object['overall_league_D']),
                overall_goals_against=int(raw_object['overall_league_GA']),
                overall_goals_for=int(raw_object['overall_league_GF']),
            ).model_dump())

        return processed_objects
