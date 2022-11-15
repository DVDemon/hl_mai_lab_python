from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .database import Base


class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)


class Destination(Base):
    __tablename__ = "destination"

    dest_id = Column(Integer, primary_key=True, index=True)
    dest_name = Column(String)


class Route(Base):
    __tablename__ = "route"

    route_id = Column(Integer, primary_key=True, index=True)
    start_point_id = Column(ForeignKey("destination.dest_id"))
    end_point_id = Column(ForeignKey("destination.dest_id"))


class Trip(Base):
    __tablename__ = "trip"

    trip_id = Column(Integer, primary_key=True, index=True)
    route_id = Column(ForeignKey("route.route_id"))
    trip_date = Column(Date)


class Person_Trip(Base):
    __tablename__ = "person_trip"

    person_id = Column(ForeignKey("person.person_id"), primary_key=True)
    trip_id = Column(ForeignKey("trip.trip_id"), primary_key=True)
