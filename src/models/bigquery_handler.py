from os import getenv

from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
from src.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

project_id = getenv("BIGQUERY_PROJECT_ID")

class BigQueryHandler:
    """
    BigQuery helper for:
    - Batch inserts with load_table_from_json
    - Query helpers (get_one, get_by_params, get_all)
    """

    def __init__(self):
        self.project_id = project_id
        self.client = bigquery.Client()
        logger.info(f"Successfully connected to BigQuery project, project_id: {project_id}")


    def _normalize_table(self, table_name: str) -> str:
        """
        Allows using:
        - project.dataset.table
        - dataset.table  (auto-add project)
        """
        parts = table_name.split(".")
        if len(parts) == 3:
            return table_name
        elif len(parts) == 2:
            dataset, table = parts
            return f"{self.project_id}.{dataset}.{table}"
        else:
            raise ValueError(f"Invalid table name: {table_name}")


    def insert_batch(self, table_name: str, rows: list[dict]):
        """
        Uses load_table_from_json
        """
        full_table_id = self._normalize_table(table_name)
        print("table:", full_table_id)

        try:
            job = self.client.load_table_from_json(
                rows,
                full_table_id,
                job_config=bigquery.LoadJobConfig(
                    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
                )
            )
            job.result()
            return True

        except GoogleAPIError as e:
            logger.error(f"BigQuery insert error: {e}")
            raise RuntimeError(f"BigQuery insert failed: {e}") from e

    def get_all(self, table_name: str):
        try:
            full_table_id = self._normalize_table(table_name)
            query = f"SELECT * FROM `{full_table_id}`"
            result = self.client.query(query).result()
            return [dict(row) for row in result]

        except GoogleAPIError as e:
            logger.error(f"BigQuery get_all error: {e}")
            raise RuntimeError(f"BigQuery query failed: {e}") from e

    def get_one(self, table_name: str, params: dict):
        """
        Returns the first matching item or None.
        """
        result = self.get_by_params(table_name, params)
        return result[0] if result else None

    def get_by_params(self, table_name: str, params: dict):
        """
        Converts params dict → WHERE conditions with safe named parameters.
        Example:
            {"status": "active", "age": 20} →
            WHERE status = @status AND age = @age
        """
        full_table_id = self._normalize_table(table_name)

        where_clause = " AND ".join([f"{k} = @{k}" for k in params.keys()])
        query = f"SELECT * FROM `{full_table_id}` WHERE {where_clause}"

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(k, "STRING", v) if isinstance(v, str)
                else bigquery.ScalarQueryParameter(k, "INT64", v)
                for k, v in params.items()
            ]
        )

        try:
            result = self.client.query(query, job_config=job_config).result()
            return [dict(row) for row in result]

        except GoogleAPIError as e:
            logger.error(f"BigQuery get_by_params error: {e}")
            raise RuntimeError(f"BigQuery query failed: {e}") from e
