from flask_jwt_extended import get_jwt_identity, create_access_token
from flask import jsonify

def initiateRefreshToken() :
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)
