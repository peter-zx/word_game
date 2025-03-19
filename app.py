from flask import Flask, send_from_directory, request, jsonify
from api.words import words_api
from api.game import game_api
from api.scores import scores_api
import os
import glob
import pandas as pd

app = Flask(__name__, static_folder='static')

app.register_blueprint(words_api)
app.register_blueprint(game_api)
app.register_blueprint(scores_api)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload_words', methods=['POST'])
def upload_words():
    os.makedirs(DATA_DIR, exist_ok=True)
    existing_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv'))
    new_file_num = len(existing_files) + 1
    new_file = os.path.join(DATA_DIR, f'words{new_file_num}.csv')

    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.csv'):
            # 读取文件内容并添加表头
            content = file.read().decode('utf-8').strip()
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write('english,chinese,difficulty\n' + content)
    elif 'text' in request.form:
        text = request.form['text'].strip()
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write('english,chinese,difficulty\n' + text)
    else:
        return jsonify({'error': 'Invalid input'}), 400

    update_game_words()
    return jsonify({'message': f'Words added to {new_file}'})

def update_game_words():
    default_file = os.path.join(DATA_DIR, 'default_words.csv')
    game_file = os.path.join(DATA_DIR, 'game_words.csv')
    word_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv'))

    all_words = []
    if word_files:
        for wf in word_files:
            try:
                df = pd.read_csv(wf)
                all_words.extend(df.to_dict(orient='records'))
            except Exception as e:
                print(f"Error reading {wf}: {e}")
    else:
        if not os.path.exists(default_file):
            default_data = [
                {'english': 'apple', 'chinese': '苹果', 'difficulty': 'L1'},
                {'english': 'banana', 'chinese': '香蕉', 'difficulty': 'L1'},
                {'english': 'cat', 'chinese': '猫', 'difficulty': 'L2'},
                {'english': 'dog', 'chinese': '狗', 'difficulty': 'L2'},
                {'english': 'elephant', 'chinese': '大象', 'difficulty': 'L3'}
            ]
            pd.DataFrame(default_data).to_csv(default_file, index=False, encoding='utf-8')
        try:
            df = pd.read_csv(default_file)
            all_words = df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading default file: {e}")
            all_words = []

    if all_words:
        df = pd.DataFrame(all_words)
        df.to_csv(game_file, index=False, encoding='utf-8')
        print(f"Updated {game_file} with {len(all_words)} words")
    else:
        print("No words available to update game_words.csv")

if __name__ == '__main__':
    update_game_words()
    app.run(debug=True)