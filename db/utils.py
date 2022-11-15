from sqlalchemy.orm import Session
from . import models, crud


def get_user_params(db: Session, db_user: models.Person):
    return {
        "id": db_user.person_id,
        "login": db_user.login,
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
    }


def get_route_params(db: Session, db_route: models.Route):
    start = crud.get_destination(db, db_route.start_point_id).dest_name
    end = crud.get_destination(db, db_route.end_point_id).dest_name
    return {"id": db_route.route_id, "start": start, "end": end}


def get_trip_params(db: Session, db_trip: models.Trip):
    db_route = crud.get_route(db, db_trip.route_id)
    route_params = get_route_params(db, db_route)
    return {
        "id": db_trip.trip_id,
        "date": db_trip.trip_date,
        "start": route_params["start"],
        "end": route_params["end"],
    }
