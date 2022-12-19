import time
import json
import sys
import signal

from kafka import KafkaConsumer

from db import crud, models
from db.database import SessionLocal, engine

# Connect to the Kafka cluster
consumer = KafkaConsumer("my-topic", bootstrap_servers=["localhost:9092"])

# Connect to the database
models.Base.prepare(autoload_with=engine)
db = SessionLocal()


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == "y":
        db.close()
        sys.exit()


signal.signal(signal.SIGINT, handler)

while True:
    # Get the latest message
    message = next(consumer)

    # Deserialize the message value
    data = json.loads(message.value.decode("utf-8"))
    print(data)

    # Extract the values from the data dictionary
    db_user = crud.get_user_by_login(db, login=data["login"])
    if not db_user:
        db_user = crud.create_user(
            db=db,
            login=data["login"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
        )

    # Sleep for 5 seconds
    time.sleep(5)
