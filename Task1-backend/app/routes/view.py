import os
from flask import jsonify, request, current_app, send_from_directory
from flask_jwt_extended import get_jwt_identity
from app.utils.helpers import dbConnection

def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


def fileView():
    username = get_jwt_identity()
    search_query = request.args.get('search', '')

    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)
    if search_query:
        cursor.execute(
            "SELECT * FROM files WHERE username = %s AND file_name LIKE %s",
            (username, f"%{search_query}%")
        )
    else:
        cursor.execute("SELECT * FROM files WHERE username = %s", (username,))
    files = cursor.fetchall()

    file_list = [
        {
            'filename' : file['file_name'],
            'filepath': os.path.join(current_app.config['UPLOAD_FOLDER'], file['file_name'])
        }
        for file in files
    ]

    return jsonify(file_list), 200