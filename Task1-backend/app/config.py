import os
from datetime import timedelta

class DbConfig :
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '12345678'
    MYSQL_DB = 'FileManagement'

class AccessKeyConfig :
    JWT_SECRET_KEY = 'FileManagementProjectWithFlaskAndReact'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class Crud :
    UPLOAD_FOLDER = os.path.join(os.getcwd(),'uploadedFiles')