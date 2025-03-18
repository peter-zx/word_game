from flask import Blueprint, jsonify, request
import pandas as pd
import random
import os

game_api = Blueprint('game_api', __name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_game_words():
    game_file = os.path.join(DATA_DIR, 'game_words.csv')
    try:
        df = pd.read_csv(game_file)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Game words file not found: {game_file}")
        return []
    except Exception as e:
        print(f"Error loading game words: {e}")
        return []

def generate_game(words, rows):
    pair_count = min(rows, len(words))
    selected_words = random.sample(words, pair_count)
    game_items = []
    for word in selected_words:
        game_items.append({'type': 'english', 'value': word['english'], 'pair': word['chinese']})
        game_items.append({'type': 'chinese', 'value': word['chinese'], 'pair': word['english']})
    random.shuffle(game_items)
    game_grid = []
    word_ids = {}
    for i, item in enumerate(game_items):
        word_ids[i] = item
        game_grid.append({'id': i, 'value': item['value']})
    return game_grid, word_ids

@game_api.route('/game/<level>', methods=['GET'])
def get_game(level):
    words = load_game_words()
    if not words:
        return jsonify({'error': 'No words found'}), 404

    level_map = {'lv1': 4, 'lv2': 5, 'lv3': 6, 'lv4': 7, 'lv5': 8, 'lv6': 9}
    rows = level_map.get(level.lower(), 4)
    groups = []
    group_count = 6 if level != 'endless' else 1
    for _ in range(group_count):
        grid, word_ids = generate_game(words, rows)
        groups.append({'grid': grid, 'word_ids': word_ids})
    return jsonify({'groups': groups, 'rows': rows})

@game_api.route('/next_group/<level>', methods=['GET'])
def next_group(level):
    words = load_game_words()
    if not words:
        return jsonify({'error': 'No words found'}), 404
    level_map = {'lv1': 4, 'lv2': 5, 'lv3': 6, 'lv4': 7, 'lv5': 8, 'lv6': 9}
    rows = level_map.get(level.lower(), 4)
    grid, word_ids = generate_game(words, rows)
    return jsonify({'grid': grid, 'word_ids': word_ids})

@game_api.route('/check', methods=['POST'])
def check_pair():
    data = request.get_json()
    word1_id = data.get('word1_id')
    word2_id = data.get('word2_id')
    word_ids = data.get('word_ids')

    if word1_id is None or word2_id is None or word_ids is None:
        return jsonify({'error': 'Invalid request'}), 400

    word1 = word_ids.get(str(word1_id))
    word2 = word_ids.get(str(word2_id))

    if word1 is None or word2 is None:
        return jsonify({'error': 'Invalid word IDs'}), 400

    if word1['value'] == word2['pair'] and word2['value'] == word1['pair']:
        return jsonify({'result': True})
    return jsonify({'result': False})