from flask import Blueprint
from app.routes.login import validateLogin
from app.routes.refreshToken import initiateRefreshToken
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/', methods = ['POST'])
def login() :
    return validateLogin()

@auth_bp.route('/refresh', methods = ['POST'])
@jwt_required()
def refresh() :
    return initiateRefreshToken()