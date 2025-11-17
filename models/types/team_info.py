from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


class TeamInfo(BaseModel):
    id: StrictInt
    name: StrictStr
    country: StrictStr
    founded: Optional[StrictInt]
    venue_name: Optional[StrictStr]
    venue_address: Optional[StrictStr]
    venue_city: Optional[StrictStr]
    venue_capacity: Optional[StrictInt]
    venue_surface: Optional[StrictStr]
    league_id: StrictInt
    league_name: StrictStr
    league_country: StrictStr
    rank: StrictInt
    points: StrictInt
    overall_wins: StrictInt
    overall_draws: StrictInt
    overall_loses: StrictInt
    overall_goals_for: StrictInt
    overall_goals_against: StrictInt
