import os
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import dbConnection

def fileDelete():
    data = request.get_json()
    filename = data.get('filename')
    username = get_jwt_identity()

    if not filename :
        return jsonify({"message" : "filename not provided"}), 400
    
    conn = dbConnection()
    cursor = conn.cursor()

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not file_path:
        conn.close()
        cursor.close()
        return jsonify({"message" : "file not found"}), 404
    
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    cursor.execute("DELETE FROM files WHERE file_name = %s AND username = %s", (filename, username))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message" : "file deleted successfully"}), 200
