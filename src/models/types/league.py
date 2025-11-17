from pydantic import BaseModel, StrictInt, StrictStr

from src.models.types.standing import Standing


class League(BaseModel):
    league_id: StrictInt
    league_name: StrictStr
    league_country: StrictStr
    league_standings: Standing
