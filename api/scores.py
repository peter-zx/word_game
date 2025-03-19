from flask import Blueprint, jsonify, request
import os
import json
import time

scores_api = Blueprint('scores_api', __name__)

@scores_api.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    score_entry = {
        'time_mode': data['time_mode'],
        'level': data['level'],
        'score': data['score'],
        'timestamp': int(time.time())
    }
    scores_file = os.path.join('data', 'scores.json')
    os.makedirs('data', exist_ok=True)  # 确保目录存在
    scores = []
    if os.path.exists(scores_file):
        with open(scores_file, 'r', encoding='utf-8') as f:
            scores = json.load(f)
    scores.append(score_entry)
    scores = sorted(scores, key=lambda x: x['timestamp'], reverse=True)[:5]
    with open(scores_file, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False)
    return jsonify({'message': 'Score saved'})

@scores_api.route('/get_scores', methods=['GET'])
def get_scores():
    scores_file = os.path.join('data', 'scores.json')
    if os.path.exists(scores_file):
        with open(scores_file, 'r', encoding='utf-8') as f:
            scores = json.load(f)
        return jsonify(scores)
    return jsonify([])