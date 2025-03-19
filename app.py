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
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file'}), 400

    new_file = os.path.join(DATA_DIR, file.filename)
    file.save(new_file)

    error = validate_csv(new_file)
    if error:
        os.remove(new_file)
        return error

    update_game_words()
    return jsonify({'message': 'Words added successfully'})

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({'error': f'Invalid CSV file: {e}'}), 400

    if not all(col in df.columns for col in ['english', 'chinese', 'difficulty']):
        return jsonify({'error': 'Missing required columns: english, chinese, difficulty'}), 400

    return None

def update_game_words():
    game_file = os.path.join(DATA_DIR, 'game_words.csv')
    word_files = glob.glob(os.path.join(DATA_DIR, 'user_words_*.csv'))
    default_file = os.path.join(DATA_DIR, 'default_words.csv')

    all_words = []
    for wf in word_files:
        try:
            df = pd.read_csv(wf)
            all_words.extend(df.to_dict(orient='records'))
        except Exception as e:
            print(f"Error reading {wf}: {e}")

    if not all_words:
        try:
            df = pd.read_csv(default_file)
            all_words = df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading default file: {e}")
            all_words = []

    if all_words:
        df = pd.DataFrame(all_words)
        df.to_csv(game_file, index=False, encoding='utf-8')
        print(f"Generated {game_file} with {len(all_words)} words")
    else:
        print("No words available to update game_words.csv")

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    update_game_words()
    app.run(debug=True)