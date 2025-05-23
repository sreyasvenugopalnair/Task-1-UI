import mysql.connector
from app.config import DbConfig
from flask import current_app

#DATABASE INITIALISATION
def dbConnection():
    conn = mysql.connector.connect(
        host = current_app.config['MYSQL_HOST'],
        username = current_app.config['MYSQL_USER'],
        password = current_app.config['MYSQL_PASSWORD'],
        database = current_app.config['MYSQL_DB']
    )
    return conn
    