from flask import jsonify, request
from app.utils.helpers import dbConnection
from flask_jwt_extended import create_access_token, create_refresh_token

def validateLogin():
    # if request.method == 'OPTIONS' :
    #     return '', 200
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Login WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user is not None :
        cursor.execute("SELECT password FROM Login WHERE username = %s", (username,))
        passwordOg = cursor.fetchone()

        if passwordOg[0] == password :
            access_token = create_access_token(identity=user[1])
            refresh_token = create_refresh_token(identity=user[1])
            
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        
        return jsonify({"error" : "password match failed"}), 400
    
    return jsonify({"error" : "invalid credentials"}), 400