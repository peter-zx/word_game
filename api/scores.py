from flask import Blueprint, jsonify, request
import json
import os

scores_api = Blueprint('scores_api', __name__)
SCORES_FILE = 'scores.json'

def load_scores():
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

@scores_api.route('/get_scores', methods=['GET'])
def get_scores():
    scores = load_scores()
    return jsonify(scores)

@scores_api.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    scores = load_scores()
    scores.append(data)
    save_scores(scores)
    return jsonify({'message': 'Score saved successfully'})