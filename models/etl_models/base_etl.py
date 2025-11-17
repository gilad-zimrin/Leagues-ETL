import asyncio
from abc import ABC, abstractmethod
from os import getenv
from typing import List, Any, Dict
from uuid import uuid4

from models.big_query_handler import BigQueryHandler
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

team_info_table = getenv('TEAM_INFO_TABLE')


class BaseETL(ABC):
    def __init__(self):
        self.etl_instance_id = uuid4()
        self.bigquery_handler: BigQueryHandler = BigQueryHandler()

    @property
    @abstractmethod
    def api_host(self):
        pass

    @property
    @abstractmethod
    def current_league_id(self):
        pass

    @abstractmethod
    async def extract(self) -> Dict | List:
        pass

    @abstractmethod
    def transform(self, raw_data):
        pass


    def load(self, rows: List[Dict], table_name: str = team_info_table):
        """
        Batch load a list of validated dicts into BigQuery.
        """
        if not rows:
            return True

        try:
            self.bigquery_handler.insert_batch(table_name, rows)
        except Exception as err:
            logger.exception("An unexpected error has occurred on load function")
            raise RuntimeError(f"Failed to load data into BigQuery: {err}") from err


    async def save_raw_data(self, raw_data):
        """
        Saving raw data to BigQuery or non-rational database for monitoring, if needed
        :return:
        """
        pass


    async def execute(self):
        # try:
        logger.info("Started a new ETL instance", extra={
            'etl_instance_id': self.etl_instance_id
        })

        raw_data = await self.extract()
        logger.debug("Successfully extracted data", extra={
            'etl_instance_id': self.etl_instance_id
        })

        asyncio.create_task(self.save_raw_data(raw_data))


        processed_objects = self.transform(raw_data)
        logger.debug(f"Successfully transformed {processed_objects} rows into TeamInfo dict", extra={
            'etl_instance_id': self.etl_instance_id
        })

        self.load(processed_objects)

        logger.debug(f"Successfully loaded {processed_objects} rows into team_info table", extra={
            'etl_instance_id': self.etl_instance_id
        })

        logger.info("Successfully finished ETL process", extra={
            'etl_instance_id': self.etl_instance_id
        })
        # except (Exception,):
        #     logger.exception("An unexpected error has occurred in execute", extra={
        #         'etl_instance_id': self.etl_instance_id
        #     })



