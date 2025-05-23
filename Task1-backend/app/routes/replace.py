from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import dbConnection
from app.routes.upload import fileUpload
import os

def deleteFileForReplace(username):
    old_filename = request.form.get('old_filename')

    if not old_filename:
        return False
    
    conn = dbConnection()
    cursor = conn.cursor()

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
    
    if not file_path:
        conn.close()
        cursor.close()
        return False
    
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    cursor.execute("DELETE FROM files WHERE file_name = %s AND username = %s", (old_filename, username))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def fileReplace():
    username = get_jwt_identity()

    if deleteFileForReplace(username) == True:
        fileUpload()
        return jsonify({"message" : "file upload successful"}), 200
    else:
        return jsonify({"message" : "error in fileDelete for replacing the file"}), 400    

