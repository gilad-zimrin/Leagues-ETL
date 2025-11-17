from pydantic import BaseModel, StrictInt, StrictStr


class Venue(BaseModel):
    venue_name: StrictStr
    venue_address: StrictStr
    venue_city: StrictStr
    venue_capacity: StrictInt
    venue_surface: StrictStr
