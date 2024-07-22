from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client['game_database']

@app.route('/add_game_to_profile', methods=['POST'])
def add_game_to_profile():
    user_id = request.json['user_id']
    game_id = request.json['game_id']
    db.usergamesplayed.insert_one({'user_id': user_id, 'game_id': game_id})
    return jsonify({"message": "Game added to profile"}), 201

@app.route('/remove_game_from_profile', methods=['POST'])
def remove_game_from_profile():
    user_id = request.json['user_id']
    game_id = request.json['game_id']
    db.usergamesplayed.delete_one({'user_id': user_id, 'game_id': game_id})
    return jsonify({"message": "Game removed from profile"}), 200

if __name__ == '__main__':
    app.run(debug=True)
