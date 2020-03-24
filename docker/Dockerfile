FROM python:3.7

RUN apt update && apt install -y \
    gcc \
    gettext \
    mysql-client libmysqlclient-dev \
    sqlite3



RUN pip install mysqlclient psycopg2 django