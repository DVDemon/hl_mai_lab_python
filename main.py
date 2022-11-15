import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, utils
from db.database import SessionLocal, engine

models.Base.prepare(autoload_with=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, person_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return utils.get_user_params(db, db_user)


@app.get("/users/get_by_mask/")
def read_user_by_mask(first_name: str, last_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_mask(db, first_name, last_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User with given mask not found")
    return list(map(lambda x: utils.get_user_params(db, x), db_user))


@app.get("/users/")
def read_users(limit: int = 3, db: Session = Depends(get_db)):
    db_users = crud.get_users(db, limit=limit)
    return list(map(lambda x: utils.get_user_params(db, x), db_users))


@app.get("/users/{user_id}/trips")
def read_user_trips(user_id: int, db: Session = Depends(get_db)):
    db_trips = crud.get_trips_by_person_id(db, user_id)
    if db_trips is None:
        raise HTTPException(status_code=404, detail="No trips for this user")
    trips = list(map(lambda x: crud.get_trip(db, x.trip_id), db_trips))
    return list(map(lambda x: utils.get_trip_params(db, x), trips))


@app.get("/trips/{trip_id}")
def read_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = crud.get_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return utils.get_trip_params(db, db_trip)


@app.get("/trips/get_by_start_name/")
def read_trips_by_start(
    start_name: str, skip: int = 0, limit: int = 3, db: Session = Depends(get_db)
):
    db_trips = crud.get_trips_by_start_name(db, start_name, skip, limit)
    if db_trips is None:
        raise HTTPException(
            status_code=404, detail="Trip with given start name not found"
        )
    return list(map(lambda x: utils.get_trip_params(db, x), db_trips))


@app.get("/trips/")
def read_trips(skip: int = 0, limit: int = 3, db: Session = Depends(get_db)):
    db_trips = crud.get_trips(db, skip=skip, limit=limit)
    return list(map(lambda x: utils.get_trip_params(db, x), db_trips))


@app.get("/routes/")
def read_routes(skip: int = 0, limit: int = 3, db: Session = Depends(get_db)):
    db_routes = crud.get_routes(db, skip=skip, limit=limit)
    return list(map(lambda x: utils.get_route_params(db, x), db_routes))


@app.get("/destinations/")
def read_destinations(skip: int = 0, limit: int = 3, db: Session = Depends(get_db)):
    db_dests = crud.get_destinations(db, skip=skip, limit=limit)
    return list(map(lambda x: {"id": x.dest_id, "name": x.dest_name}, db_dests))


@app.post("/users/")
def create_user(
    login: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_login(db, login=login)
    if db_user:
        raise HTTPException(
            status_code=400, detail="User with this login already registered"
        )
    return crud.create_user(
        db=db,
        login=login,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )


@app.post("/destinations/")
def create_destination(place_name: str, db: Session = Depends(get_db)):
    db_dest = crud.get_destination_by_name(db, dest_name=place_name)
    if db_dest:
        raise HTTPException(status_code=400, detail="This place already registered")
    return crud.create_destination(db=db, dest_name=place_name)


@app.post("/routes/")
def create_route(start_id: int, end_id: int, db: Session = Depends(get_db)):
    db_route = crud.get_route_by_start_and_end(db, start_id, end_id)
    if db_route:
        raise HTTPException(status_code=400, detail="This route already registered")
    return crud.create_route(db=db, start_id=start_id, end_id=end_id)


@app.post("/trips/")
def create_trip(route_id: int, date: datetime.date, db: Session = Depends(get_db)):
    db_trip = crud.get_trip_by_route_and_date(db, route_id, date)
    if db_trip:
        raise HTTPException(status_code=400, detail="This trip already registered")
    return crud.create_trip(db=db, route_id=route_id, date=date)
