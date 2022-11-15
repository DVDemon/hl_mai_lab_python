# MySQL + FastAPI

## Create docker with ProxySQL and MySQL

- build docker:
```
cd docker
docker-compose up --build
```

- if mysql client doesn't work locally:
```
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

- to check anything in ProxySQL:
```
mysql -uradmin -pradmin -h 127.0.0.1 -P6032 --prompt='Admin> '
```

- create tables in each node and insert data in them (user: test, password: pass)
```
mysql -h 127.0.0.1 -P 3360 -e "source sql/create.sql" -u test -p 
mysql -h 127.0.0.1 -P 3361 -e "source sql/create.sql" -u test -p
mysql -h 127.0.0.1 -P 6033 -e "source sql/insert.sql" -u test -p   
```

### IMPORTANT
- if script contains two whitespaces, it get/post data in second node, else in first

## Start app

create environment and install requirements:
```
python -m venv rest
source rest/bin/activate
pip install -r requirements.txt
```

start app:
```
uvicorn main:app --reload
```

see all methods on http://127.0.0.1:8000/docs