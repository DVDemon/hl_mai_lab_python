import datetime
from pydantic import BaseModel

class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str

class Dest(BaseModel):
    dest_name: str

class Route(BaseModel):
    start_point_id: int
    end_point_id: int

class Trip(BaseModel):
    route_id: int
    trip_date: datetime.date
