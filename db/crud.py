import random
import datetime
from sqlalchemy.orm import Session
from . import models


def get_user(db: Session, person_id: int):
    first = db.execute("select * from person where person_id = %s" % person_id).first()
    if first:
        return first
    return db.execute("select  * from person where person_id = %s" % person_id).first()


def get_users(db: Session, limit: int = 5):
    first = db.execute("select * from person").all()
    second = db.execute("select  * from person").all()
    all = first + second
    return all[:limit]


def get_user_by_login(db: Session, login: str):
    first = db.execute(
        "select * from person where login = :val", {"val": login}
    ).first()
    if first:
        return first
    return db.execute(
        "select  * from person where login = :val", {"val": login}
    ).first()


def get_user_by_mask(db: Session, first_name: str, last_name: str):
    first_name_mask = "%" + first_name + "%"
    last_name_mask = "%" + last_name + "%"
    first = db.execute(
        "select * from person where first_name like :val1 and last_name like :val2",
        {"val1": first_name_mask, "val2": last_name_mask},
    ).all()
    second = db.execute(
        "select  * from person where first_name like :val1 and last_name like :val2",
        {"val1": first_name_mask, "val2": last_name_mask},
    ).all()
    return first + second


def get_destination(db: Session, dest_id: int):
    return (
        db.query(models.Destination)
        .filter(models.Destination.dest_id == dest_id)
        .first()
    )


def get_destinations(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Destination).offset(skip).limit(limit).all()


def get_destination_by_name(db: Session, dest_name: str):
    return (
        db.query(models.Destination)
        .filter(models.Destination.dest_name == dest_name)
        .first()
    )


def get_route(db: Session, route_id: int):
    return db.query(models.Route).filter(models.Route.route_id == route_id).first()


def get_routes(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Route).offset(skip).limit(limit).all()


def get_route_by_start_and_end(db: Session, start_id: int, end_id: int):
    return (
        db.query(models.Route)
        .filter(
            models.Route.start_point_id == start_id, models.Route.end_point_id == end_id
        )
        .first()
    )


def get_routes_by_start_id(db: Session, start_id: int, skip: int = 0, limit: int = 5):
    return (
        db.query(models.Route)
        .filter(models.Route.start_point_id == start_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_routes_by_start_name(
    db: Session, start_name: str, skip: int = 0, limit: int = 5
):
    right_dest = get_destination_by_name(db, start_name)
    return get_routes_by_start_id(db, right_dest.dest_id, skip, limit)


def get_trip(db: Session, trip_id: int):
    return db.query(models.Trip).filter(models.Trip.trip_id == trip_id).first()


def get_trip_by_route_and_date(db: Session, route_id: int, date: datetime.time):
    return (
        db.query(models.Trip)
        .filter(models.Trip.route_id == route_id, models.Trip.trip_date == date)
        .first()
    )


def get_trips(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Trip).offset(skip).limit(limit).all()


def get_trips_by_start_name(
    db: Session, start_name: str, skip: int = 0, limit: int = 5
):
    routes = get_routes_by_start_name(db, start_name, skip, limit)
    routes_ids = list(map(lambda x: x.route_id, routes))
    return (
        db.query(models.Trip)
        .filter(models.Trip.route_id.in_(routes_ids))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_trips_by_person_id(db: Session, person_id: int, skip: int = 0, limit: int = 5):
    return (
        db.query(models.Person_Trip)
        .filter(models.Person_Trip.person_id == person_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(
    db: Session, login: str, first_name: str, last_name: str, email: str, password: str
):
    k = random.randint(0, 1)
    person_id = len(get_users(db, limit=-1)) + 1
    db_user = models.Person(
        person_id=person_id,
        login=login,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )
    if not k:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    else:
        db.execute(
            "insert into  person (person_id, login, first_name, last_name, email, password) values (:val0, :val1, :val2, :val3, :val4, :val5);",
            {
                "val0": person_id,
                "val1": login,
                "val2": first_name,
                "val3": last_name,
                "val4": email,
                "val5": password,
            },
        )
        db.commit()
    return db_user


def create_destination(db: Session, dest_name: str):
    db_dest = models.Destination(dest_name=dest_name)
    db.add(db_dest)
    db.commit()
    db.refresh(db_dest)
    return db_dest


def create_route(db: Session, start_id: int, end_id: int):
    db_route = models.Route(start_point_id=start_id, end_point_id=end_id)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


def create_trip(db: Session, route_id: int, date: datetime.time):
    db_trip = models.Trip(route_id=route_id, trip_date=date)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip
