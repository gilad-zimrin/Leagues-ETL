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
    league_id: Optional[StrictInt]
    league_name: Optional[StrictStr]
    league_country: Optional[StrictStr]
    rank: Optional[StrictInt]
    points: Optional[StrictInt]
    overall_wins: Optional[StrictInt]
    overall_draws: Optional[StrictInt]
    overall_loses: Optional[StrictInt]
    overall_goals_for: Optional[StrictInt]
    overall_goals_against: Optional[StrictInt]
