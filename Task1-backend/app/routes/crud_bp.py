from flask import Blueprint, send_from_directory
from app.routes.upload import fileUpload
from app.routes.delete import fileDelete
from app.routes.view import fileView, uploaded_file
from app.routes.replace import fileReplace
from app.routes.download import fileDownload
from app.routes.logout import logOut
from flask_jwt_extended import jwt_required

crud_bp = Blueprint('crud',__name__)

UPLOAD_FOLDER = '/home/sreyasvnair/RS/Task1/uploadedFiles'

@crud_bp.route('/upload', methods = ['POST'])
@jwt_required()
def upload():
    return fileUpload()

@crud_bp.route('/delete', methods = ['DELETE'])
@jwt_required()
def delete():
    return fileDelete()

@crud_bp.route('/view', methods = ['GET'])
@jwt_required()
def view():
    return fileView()

@crud_bp.route('/replace', methods = ['PUT'])
@jwt_required()
def replace():
    return fileReplace()

@crud_bp.route('/uploads/<filename>')
@jwt_required()
def viewUploaded(filename):
    return uploaded_file(filename)

@crud_bp.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download(filename):
    return fileDownload(filename)

@crud_bp.route('/logout')
@jwt_required()
def logout():
    return logOut()