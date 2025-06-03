from flask import Blueprint, request, jsonify
from auth import signup, login
from db_config import get_db_connection

routes = Blueprint("routes", __name__)

@routes.route('/signup', methods=['POST'])
def signup_route():
    data = request.json
    return jsonify(signup(data["username"], data["password"]))

@routes.route('/login', methods=['POST'])
def login_route():
    data = request.json
    return jsonify(login(data["username"], data["password"]))

@routes.route('/save_score', methods=['POST'])
def save_score():
    db = get_db_connection()
    cursor = db.cursor()
    data = request.json
    username = data.get('username')
    score = data.get('score')

    cursor.execute("UPDATE game_data SET high_score = %s WHERE user_id = (SELECT id FROM players WHERE username = %s)", (score, username))
    db.commit()

    return jsonify({"message": "Score updated successfully"})

@routes.route('/get_score/<username>', methods=['GET'])
def get_score (username):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT high_score FROM game_data WHERE user_id = (SELECT id FROM players WHERE username = %s)", (username,))
    result = cursor.fetchone()
    return jsonify({"high_score": result[0]}) if result else jsonify({"error": "User not found"})