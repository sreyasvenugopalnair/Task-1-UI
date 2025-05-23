from flask import session, jsonify

def logOut():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200