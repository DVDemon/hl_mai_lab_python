# MySQL + FastAPI

## Create DB with Docker

- clone mysql image and run it:
```
sudo docker pull mysql/mysql-server:latest
sudo docker run --name=mysql --env="MYSQL_ROOT_PASSWORD=pass" --publish 6603:3306 -d mysql/mysql-server:latest
```

- if mysql client doesn't work locally:
```
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

- connect to mysql by executable image format:
```
sudo docker exec -it mysql bash
mysql -uroot -p
```

- grant access for remote (go to mysql in exec image format and write):
```
CREATE USER 'root'@'%' IDENTIFIED BY 'pass';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
```

- connect:
```
mysql -h 127.0.0.1 -P 6603 -p  
```

- create and insert all data:
```
mysql -h 127.0.0.1 -P 6603  -e "source sql/create.sql" -p
mysql -h 127.0.0.1 -P 6603  -e "source sql/insert.sql" -p
```

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