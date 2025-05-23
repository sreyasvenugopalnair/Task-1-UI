import os
from flask import Flask
from app.routes.auth_bp import auth_bp
from app.routes.crud_bp import crud_bp
from app.config import DbConfig, AccessKeyConfig, Crud
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app() :
    app = Flask(__name__)

    jwt = JWTManager(app)

    CORS(app)
    
    app.config.from_object(DbConfig)
    app.config.from_object(AccessKeyConfig)
    app.config.from_object(Crud)

    app.register_blueprint(auth_bp)
    app.register_blueprint(crud_bp)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
