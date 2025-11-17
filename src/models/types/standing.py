from pydantic import BaseModel, StrictInt, StrictStr


class Standing(BaseModel):
    rank: StrictInt
    points: StrictInt
    overall_wins: StrictInt
    overall_draws: StrictInt
    overall_loses: StrictInt
    overall_goals_for: StrictInt
    overall_goals_against: StrictInt
