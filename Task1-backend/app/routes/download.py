import os
from flask import current_app, jsonify, send_from_directory

def fileDownload(filename):
    try:
        # Check if file exists
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
            return jsonify({'message': 'File not found'}), 404

        # Send the file as an attachment (forces download)
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True), 200

    except Exception as e:
        return jsonify({'message': 'Error during file download', 'error': str(e)}), 500