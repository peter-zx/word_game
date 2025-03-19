from flask import Flask, send_from_directory, request, jsonify
from api.words import words_api
from api.game import game_api
from api.scores import scores_api  # 新增分数模块
import os

app = Flask(__name__, static_folder='static')

app.register_blueprint(words_api)
app.register_blueprint(game_api)
app.register_blueprint(scores_api)  # 注册分数模块

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

if __name__ == '__main__':
    app.run(debug=True)