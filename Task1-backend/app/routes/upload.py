import os
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.utils.helpers import dbConnection
from flask_jwt_extended import get_jwt_identity

ALLOWED_EXTENSIONS = {'img', 'jpeg', 'png', 'jpg'}
MAX_IMAGE_SIZE = 5*1024*1024

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_fileSize(file) :
    file.seek(0,os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_IMAGE_SIZE :
        return False
    else:
        return True
    

def saveToDB(filename):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (file_name, username) VALUES "
    "(%s, %s)", (filename, get_jwt_identity()))
    conn.commit()
    cursor.close()
    conn.close()


def fileUpload():
    if 'file' not in request.files:
        print("no file part in the form data")
        return jsonify({"message" : "no file part in the form"}), 400
    
    file = request.files['file']

    if file.filename == '':
        print("no file selected")
        return jsonify({"message" : "you haven't selected any file"}), 400
    
    if file and allowed_filename(file.filename):
        if allowed_fileSize(file):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            saveToDB(filename)
            return jsonify({"message" : "file uploaded successfully"}), 200
        return jsonify({"message" : "file is too large"}), 400
    else:
        return jsonify({"message" : "invalid file extension"}), 400
        