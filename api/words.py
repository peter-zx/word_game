from flask import Blueprint, jsonify, request
import pandas as pd
import os

words_api = Blueprint('words_api', __name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_words_from_csv():
    words_file = os.path.join(DATA_DIR, 'game_words.csv')
    try:
        df = pd.read_csv(words_file)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Words file not found: {words_file}")
        return []
    except Exception as e:
        print(f"Error loading words: {e}")
        return []

@words_api.route('/words', methods=['GET'])
def get_words():
    words = load_words_from_csv()
    return jsonify(words)

@words_api.route('/add_word', methods=['POST'])
def add_word():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    english = data.get('english')
    chinese = data.get('chinese')
    difficulty = data.get('difficulty')

    if not english or not chinese or not difficulty:
        return jsonify({'error': 'Missing fields'}), 400

    words = load_words_from_csv()
    words.append({'english': english, 'chinese': chinese, 'difficulty': difficulty})

    try:
        df = pd.DataFrame(words)
        df.to_csv(os.path.join(DATA_DIR, 'game_words.csv'), index=False, encoding='utf-8')
        return jsonify({'message': 'Word added successfully'})
    except Exception as e:
        return jsonify({'error': f'Error saving words: {e}'}), 500