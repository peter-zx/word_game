from flask import Flask, send_from_directory, request, jsonify
from api.words import words_api
from api.game import game_api
import os
import json

app = Flask(__name__, static_folder='static')

app.register_blueprint(words_api)
app.register_blueprint(game_api)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload_words', methods=['POST'])
def upload_words():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.csv'):
            file.save(os.path.join('data', 'words.csv'))
            return jsonify({'message': 'File uploaded successfully'})
    elif 'text' in request.form:
        text = request.form['text']
        with open('data/words.csv', 'w', encoding='utf-8') as f:
            f.write(text)
        return jsonify({'message': 'Text saved successfully'})
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    score_entry = {
        'time_mode': data['time_mode'],
        'level': data['level'],
        'score': data['score']
    }
    scores_file = os.path.join('data', 'scores.json')
    scores = []
    if os.path.exists(scores_file):
        with open(scores_file, 'r', encoding='utf-8') as f:
            scores = json.load(f)
    scores.append(score_entry)
    scores = scores[-5:]  # 保留最近 5 次
    with open(scores_file, 'w', encoding='utf-8') as f:
        json.dump(scores, f)
    return jsonify({'message': 'Score saved'})

@app.route('/get_scores', methods=['GET'])
def get_scores():
    scores_file = os.path.join('data', 'scores.json')
    if os.path.exists(scores_file):
        with open(scores_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)